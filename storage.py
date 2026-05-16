import json
from pathlib import Path
from tasks import Task, TaskList
from dataclasses import asdict

def save_tasks(task_list: TaskList, path: Path) -> None:
    data = [asdict(task)for task in task_list._tasks]
    
    with path.open("w") as file:
        json.dump(data, file, indent = 2)
        
def load_tasks(path:Path) -> dict:
    with path.open("r") as file:
         data = json.load(file)
         
    task_list = TaskList()
    
    task_list._tasks = [
        Task(
            title=item["title"],
            done=item["done"],
            id=item["id"]
        )
        for item in data
    ]

    return task_list
        
    
    