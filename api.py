# API : Application Programming Interface
# API is a set of rules and protocols that allows software applications to communicate with each other.
#
# HTTP PROTOCOL INTRODUCTION
#
# REQUEST
# METHOD ENDPOINT
#
#
# METHODS: GET, POST, PUT, DELETE, OPTIONS
# GET - Retrieve a resource
# POST - Create a resource
# PUT - Update a resource
# PATCH - Update a resource partially
# DELETE - Delete a resource
# OPTIONS - Get the supported methods for a resource
#
# URI: https://app.diagrams.net/ENDPOINT(PATH)
# URI : protocol://HOSTNAME:PORT(80-http /443 -https)/ENDPOINT/PATH
#
#
#
# RESPONSE:
# STATUS CODES: 2XX - Success, 3XX - Redirect, 4XX - Client Error, 5XX - Server Error
#
# THE CONTRACTS
# GET /tasks — list all tasks. Returns 200 with a JSON array.
# GET /tasks/{id} — get one task. Returns 200, or 404 if not found.
# POST /tasks — create a new task. Returns 201 with the created task.
# PATCH /tasks/{id}/done — mark a task done. Returns 200 with the updated task.
# DELETE /tasks/{id} — remove a task. Returns 204 (no body).
#
# INCASE OF ERROR: Returns 4XX or 5XX with an error message.

from dataclasses import asdict
from pathlib import Path
from fastapi import FastAPI, HTTPException
from tasks import Task, TaskList
from storage import load_tasks,save_tasks


api = FastAPI()

DATA = Path("tasks.json")

def _load() -> TaskList:
    # if DATA.exists():
    #     return load_tasks(DATA)
    # return TaskList()
    return load_tasks(DATA) if DATA.exists() else TaskList()

def _persist(tl: TaskList) -> None:
    save_tasks(tl, DATA)

@api.get("/tasks")
def list_tasks():
    tl = _load()
    return {"tasks": [asdict(t) for t in tl._tasks]}

# http://127.0.0.1:8000/tasks/1uigg6
@api.get("/tasks/{task_id}")
def get_task(task_id: str):
    tl = _load()
    try:
        return asdict(tl.get_by_id(task_id))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"task {task_id} not found")

@api.post(f"/tasks", status_code=201)
def create_task(payload: dict):
    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    tl = _load()
    task = Task(title=title)
    tl.add(task)
    _persist(tl)
    return asdict(task)
