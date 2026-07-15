import pytest

from storage import load_tasks, save_tasks
from tasks import Task, TaskList


def test_save_then_load_round_trip(tmp_path):
    path = tmp_path / "tasks.json"

    original = TaskList()
    original.add(Task(title="Buy milk", user_id="user-1"))
    original.add(Task(title="Write tests", user_id="user-1"))

    save_tasks(original, path)
    loaded = load_tasks(path)

    assert len(loaded) == len(original)
    assert loaded._tasks[0].title == "Buy milk"
    assert loaded._tasks[1].title == "Write tests"
    assert loaded._tasks[0].done is False


def test_load_missing_file_raises_filenotfounderror(tmp_path):
    missing_path = tmp_path / "does-not-exist.json"

    with pytest.raises(FileNotFoundError):
        load_tasks(missing_path)
