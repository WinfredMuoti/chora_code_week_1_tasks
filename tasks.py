from dataclasses import dataclass, field
from uuid import uuid4
@dataclass
class Task:
    title: str
    done: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    
    def mark_done(self) -> None:
        self.done = True
    
class TaskList:
    def __init__(self) -> None:
        self._tasks: list [Task] = []
        
    def __len__(self) -> int:
        return len(self._tasks) 
    
    def add(self, task:Task) -> None:
        self._tasks.append(task)

    def get_by_id(self, task_id: str) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        else:
            raise KeyError(task_id)
        
