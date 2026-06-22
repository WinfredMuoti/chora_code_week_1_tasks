from typing import Any, Iterator

from sqlalchemy.orm import Session

from database import SessionLocal, TaskModel
from tasks import Task, TaskList


def _task_model_to_task(row: TaskModel) -> Task:
    return Task(
        id=row.id,
        title=row.title,
        done=row.done,
        created_at=row.created_at,
    )


def _task_to_task_model(task: Task) -> TaskModel:
    return TaskModel(
        id=task.id,
        title=task.title,
        done=task.done,
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


def update_task(db: Session, task: Task) -> None:
    row = db.get(TaskModel, task.id)

    if row is None:
        raise KeyError(task.id)

    row.done = task.done
    row.title = task.title

    db.commit()


def delete_task(db: Session, task_id: str) -> None:
    row = db.get(TaskModel, task_id)

    if row is None:
        raise KeyError(task_id)

    db.delete(row)
    db.commit()
