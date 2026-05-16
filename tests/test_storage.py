import pytest
from tasks import Task, TaskList
from storage import save_tasks, load_tasks

def test_save_then_load_round_trip(tmp_path):
    path = tmp_path / "tasks.json"
 
    original = TaskList()
    original.add(Task(title="Buy milk"))
    original.add(Task(title="Write tests"))
 
    save_tasks(original, path)
    loaded = load_tasks(path)
 
    assert len(loaded) == len(original)
    assert loaded._tasks[0].title == "Buy milk"
    assert loaded._tasks[1].title == "Write tests"
    assert loaded._tasks[0].done is False