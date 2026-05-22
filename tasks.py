from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Task:
    title: str
    done: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))

    def mark_done(self) -> None:
        """marks a task as completed"""
        self.done = True


class TaskList:
<<<<<<< HEAD
    
=======

>>>>>>> e0a89c4 (fix: align TaskList behavior with tests and improve core logic)
    def __init__(self) -> None:
        """creates an empty task list"""
        self._tasks: list[Task] = []

    def __len__(self) -> int:
        """returns the number of tasks"""
        return len(self._tasks)

    def add(self, task: Task) -> None:
        """adds a task to the list"""
        self._tasks.append(task)

    def get_by_id(self, task_id: str) -> Task:
        """finds and returns a task by it's id"""
        for task in self._tasks:
            if task.id == task_id:
                return task

        raise KeyError(task_id)

    def complete(self, task_id: str) -> Task:
        """marks a specific task as done"""
        task = self.get_by_id(task_id)
        task.mark_done()
        return task

    def remove(self, task_id: str) -> None:
        """deletes a task from the lis"""
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                return

        raise ValueError("Task not found")
