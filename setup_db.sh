#!/usr/bin/env bash
#
# setup_db.sh — one-shot Postgres setup for the tasks app, inside WSL/Ubuntu.
#
# Installs Postgres, starts it, and creates a `tasks` user + `tasks` database
# on port 5454 so the connection string matches compose.yml exactly:
#
#     postgresql://tasks:tasks@localhost:5454/tasks
#
# Safe to run more than once — every step is idempotent.
#
# Usage:  ./setup_db.sh
#
set -euo pipefail

DB_USER="tasks"
DB_PASS="tasks"
DB_NAME="tasks"
DB_PORT="5454"

say()  { printf '\n\033[1;34m==>\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m  ok\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m  !!\033[0m %s\n' "$*"; }

# --- sanity: not as root, but sudo must work -------------------------------
if [[ "${EUID}" -eq 0 ]]; then
  warn "Run as your normal user (the script calls sudo itself), not as root."
  exit 1
fi

# --- 1. install ------------------------------------------------------------
if ! command -v psql >/dev/null 2>&1; then
  say "Installing Postgres (this is the slow part)…"
  sudo apt update
  sudo apt install -y postgresql postgresql-contrib
  ok "Postgres installed."
else
  ok "Postgres already installed — skipping apt."
fi

# Find the installed cluster (version dir under /etc/postgresql).
PG_VER="$(ls /etc/postgresql 2>/dev/null | sort -V | tail -n1 || true)"
if [[ -z "${PG_VER}" ]]; then
  warn "No Postgres cluster found under /etc/postgresql. Install may have failed."
  exit 1
fi
ok "Using cluster: version ${PG_VER}, main."

# --- 2. set the port to 5454 (match compose.yml) ---------------------------
say "Setting listen port to ${DB_PORT}…"
sudo pg_conftool "${PG_VER}" main set port "${DB_PORT}"
ok "Port set."

# --- 3. start the server ---------------------------------------------------
# WSL usually has no systemd, so use the service wrapper (works either way).
say "Starting Postgres…"
sudo service postgresql restart
# Give it a moment to bind the socket.
for _ in $(seq 1 10); do
  if sudo -u postgres psql -p "${DB_PORT}" -c '\q' 2>/dev/null; then break; fi
  sleep 1
done
ok "Postgres is up on port ${DB_PORT}."

# --- 4. create role + database (idempotent) --------------------------------
say "Creating role '${DB_USER}' and database '${DB_NAME}'…"

# Role: create if missing, always (re)set the password so it's predictable.
sudo -u postgres psql -p "${DB_PORT}" -v ON_ERROR_STOP=1 <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '${DB_USER}') THEN
    CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASS}';
  ELSE
    ALTER ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASS}';
  END IF;
END
\$\$;
SQL
ok "Role ready."

# Database: createdb errors if it exists, so guard it.
if sudo -u postgres psql -p "${DB_PORT}" -tAc \
     "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | grep -q 1; then
  ok "Database '${DB_NAME}' already exists."
else
  sudo -u postgres createdb -p "${DB_PORT}" -O "${DB_USER}" "${DB_NAME}"
  ok "Database '${DB_NAME}' created, owned by '${DB_USER}'."
fi

# --- 5. sanity check: connect over TCP as the app would --------------------
say "Verifying TCP login (the way your app connects)…"
if PGPASSWORD="${DB_PASS}" psql -h localhost -p "${DB_PORT}" \
     -U "${DB_USER}" -d "${DB_NAME}" -c 'SELECT version();' >/dev/null 2>&1; then
  ok "Login works."
else
  warn "TCP login failed. Check pg_hba.conf in /etc/postgresql/${PG_VER}/main/"
  warn "(local installs usually allow md5/scram on localhost out of the box)."
  exit 1
fi

cat <<DONE

------------------------------------------------------------------
  Done. Your database is ready.

  Connection string:
      postgresql://${DB_USER}:${DB_PASS}@localhost:${DB_PORT}/${DB_NAME}

  Open a SQL shell:
      psql -h localhost -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME}
      (password: ${DB_PASS})

  Start / stop the server later:
      sudo service postgresql start
      sudo service postgresql stop
------------------------------------------------------------------
DONE
