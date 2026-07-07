# Chora Week 1 — Task Manager

A task management application built as part of Chora Code Academy's Python track.

The project started as a CLI task manager and has been extended with FastAPI and PostgreSQL persistence. Development follows a test-first approach using Pytest.

## Features

* Create tasks
* List tasks
* Update tasks
* Mark tasks as complete
* Delete tasks
* Store tasks in PostgreSQL

## Technologies

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pytest

## Project Structure

```text
api.py          # FastAPI endpoints
repository.py   # Database access layer
database.py     # SQLAlchemy models and configuration
tasks.py        # Domain models
storage.py      # File storage implementation
tests/          # Automated tests
```

## Setup

```bash
python3 -m venv .venv #
source .venv/bin/activate
pip install -r requirements.txt
```

## Run~ Tests

```bash
pytest -v
```

## Run Application

```bash
fastapi dev
```
