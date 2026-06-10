from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException

from storage import load_tasks, save_tasks
from tasks import Task, TaskList
from schemas import TaskCreate, TaskResponse, TaskListResponse

app = FastAPI(title="Task Manager API")

DATA = Path("tasks.json")


def _load() -> TaskList:
    return load_tasks(DATA) if DATA.exists() else TaskList()


def _persist(tl: TaskList) -> None:
    save_tasks(tl, DATA)


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/tasks", response_model=TaskListResponse)
def list_tasks():
    tl = _load()
    return {"tasks": tl._tasks}


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    tl = _load()

    try:
        task = tl.get_by_id(task_id)
        return task

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(payload: TaskCreate):
    tl = _load()
    task = Task(title=payload.title)
    tl.add(task)
    _persist(tl)
    return task



@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: str):
    tl = _load()

    try:
        task = tl.complete(task_id)

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    _persist(tl)

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    tl = _load()

    try:
        tl.remove(task_id)

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    _persist(tl)