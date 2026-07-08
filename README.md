# Chora Week 1 — Task Manager

A task management application built as part of Chora Code Academy's Python track.

The project started as a CLI task manager and has been extended with FastAPI and PostgreSQL persistence. Development follows a test-first approach using Pytest.

## Features

* Create tasks
* List tasks
* Update tasks
* Mark tasks as complete
* Delete tasks
* update tasks title
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
1. Clone the repository

First, download the project to your computer using Git.

git clone <repository-url>

Replace <repository-url> with the URL of this GitHub repository.

2. Navigate into the project folder

Move into the project directory so all commands run inside the project.

cd <project-folder>

Replace <project-folder> with the name of the folder created after cloning the repository.

3. Create a virtual environment

A virtual environment creates an isolated space for this project's Python packages. This prevents conflicts with packages installed for other Python projects.
```bash
python3 -m venv .venv
```
4. Activate the virtual environment

Before installing dependencies or running the project, activate the virtual environment.

Linux/macOS:
```bash
source .venv/bin/activate
```
Windows:

.venv\Scripts\activate

#After activation, your terminal should display (.venv) at the beginning of the command line, indicating that the virtual environment is active.

5.  Install project dependencies

Install all the required Python packages listed in requirements.txt.

pip install -r requirements.txt

Wait for the installation to finish before moving to the next step.

Run Tests

Run the automated test suite to verify that everything is working correctly.

pytest -v

If all tests pass, you should see a summary showing that every test completed successfully.

# Run Application

Start the FastAPI development server.

fastapi dev

Once the server starts, open your browser and visit:

http://127.0.0.1:8000/docs — Interactive Swagger API documentation where you can test every endpoint.
http://127.0.0.1:8000/redoc — Alternative API documentation in a clean, read-only format.

## API Reference

### Endpoints

| Method | Path | Description | Success | Error |
|--------|------|-------------|---------|-------|
| GET | `/` | Health check | `200 OK` | - |
| GET | `/tasks` | List all tasks | `200 OK` | - |
| GET | `/tasks/{task_id}` | Get a task by ID | `200 OK` | `404 Not Found` |
| POST | `/tasks` | Create a new task | `201 Created` | `400 Bad Request` |
| PATCH | `/tasks/{task_id}/complete` | Mark a task as complete | `200 OK` | `404 Not Found` |
| PATCH | `/tasks/{task_id}/title` | Rename a task | `200 OK` | `404 Not Found` |
| DELETE | `/tasks/{task_id}` | Delete a task | `204 No Content` | `404 Not Found` |

### Sample Task JSON

```json
{
  "id": "2c9d6a93-1d1b-4a67-b4de-58dd3d95cb2e",
  "title": "Buy groceries",
  "done": false,
  "created_at": "2026-07-08T10:30:15.123456"
}
```

### cURL Examples

#### Create a task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Buy groceries"}'
```

#### Complete a task

```bash
curl -X PATCH http://localhost:8000/tasks/<task_id>/complete
```

Replace `<task_id>` with the task ID.

#### Rename a task

```bash
curl -X PATCH http://localhost:8000/tasks/<task_id>/title \
-H "Content-Type: application/json" \
-d '{"title":"Buy groceries and fruit"}'
```

Replace `<task_id>` with the task ID.

#### Delete a task

```bash
curl -X DELETE http://localhost:8000/tasks/<task_id>
```

Replace `<task_id>` with the task ID.
