import json
from pathlib import Path
from dataclasses import asdict
from datetime import datetime

from tasks import Task, TaskList


def save_tasks(task_list: TaskList, path: Path) -> None:
    data = [asdict(task) for task in task_list._tasks]
    with path.open("w") as file:
        json.dump(data, file, indent=2, default=str)

def load_tasks(path: Path) -> TaskList:
    with path.open("r") as file:
        data = json.load(file)

    task_list = TaskList()

    for item in data:
        created_at = item.get("created_at", "2026-01-01")
        task = Task(
            title=item["title"],
            done=item["done"],
            id=item["id"],
            created_at=datetime.fromisoformat(created_at),
        )
        task_list._tasks.append(task)
        
    return task_list
