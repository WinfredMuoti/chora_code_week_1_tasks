from dataclasses import dataclass, field
from uuid import uuid4
@dataclass
class Task:
    title: str
    done: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    
    def mark_done(self) -> None:
        self.done = True
    
class Tasklist:
    def __init__(self) -> None:
        self._tasks: list [Task] = []
        
    def __len__(self) -> int:
        return len(self._tasks)   
        
        
