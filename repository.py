from typing import Any, Iterator

from sqlalchemy.orm import Session

from database import SessionLocal, TaskModel
from tasks import Task, TaskList


def _task_model_to_task(row: TaskModel) -> Task:
    return Task(
        id=row.id,
        title=row.title,
        done=row.done,
        user_id=row.user_id,
        created_at=row.created_at,
    )


def _task_to_task_model(task: Task) -> TaskModel:
    return TaskModel(
        id=task.id,
        title=task.title,
        done=task.done,
        user_id=task.user_id,
        created_at=task.created_at,
    )


def get_database_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_all_tasks(db: Session) -> TaskList:
    tl = TaskList()

    for row in db.query(TaskModel).all():
        tl.add(_task_model_to_task(row))

    return tl


def create_task(db: Session, task: Task) -> None:
    db.add(_task_to_task_model(task))
    db.commit()


def get_task_by_id(db: Session, task_id: str) -> Any:
    row = db.get(TaskModel, task_id)
    if row is None:
        raise KeyError(task_id)
    return row


def update_task(db: Session, task_id: str) -> None:
    row = db.get(TaskModel, task_id)
    if row is None:
        raise KeyError(task_id)
    row.done = True
    db.commit()

def update_task_title(db: Session, task_id: str, title: str) -> None:
    row = db.get(TaskModel, task_id)

    if row is None:
        raise KeyError(task_id)

    row.title = title
    db.commit()


def delete_task(db: Session, task_id: str) -> None:
    row = db.get(TaskModel, task_id)
    if row is None:
        raise KeyError(task_id)
    db.delete(row)
    db.commit()


#create def update task title, update readme file,update commit,
