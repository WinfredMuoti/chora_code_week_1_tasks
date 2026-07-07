# from dataclasses import asdict

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import create_tables
from repository import (
    _task_model_to_task,
    create_task,
    delete_task,
    get_all_tasks,
    get_database_session,
    get_task_by_id,
    update_task,
     update_task_title
)
from schemas import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from tasks import Task  # TaskList

app = FastAPI(title="Task Manager API")


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/tasks", response_model=TaskListResponse)
def list_tasks(db: Session = Depends(get_database_session)):
    tl = get_all_tasks(db)
    return {"tasks": tl._tasks}


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_database_session)):
    try:
        task = get_task_by_id(db, task_id)
        return task
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_new_task(payload: TaskCreate, db: Session = Depends(get_database_session)):
    try:
        dummy_id = "123"
        task = Task(title=payload.title, user_id=dummy_id)
        create_task(db, task)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: str, db: Session = Depends(get_database_session)):
    try:
        update_task(db, task_id)

        return get_task_by_id(db, task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: str, db: Session = Depends(get_database_session)):
    try:
        delete_task(db, task_id)

    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}/title", response_model=TaskResponse)
def change_task_title(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_database_session),
):
    try:
        update_task_title(db, task_id, payload.title)

        return get_task_by_id(db, task_id)

    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
