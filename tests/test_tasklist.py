from tasks import TaskList
from tasks import Task

import pytest

@pytest.fixture
def populated_list() -> TaskList:
    t1 = TaskList()
    t1.add(Task(title="Buy milk"))
    t1.add(Task(title="Write tests"))
    return t1

def test_new_list_is_empty():
    t1 = TaskList()
    assert len(t1) == 0
    
def test_add_increases_length():
    t1 = TaskList()
    t1.add(Task(title="Buy milk"))
    assert len(t1) == 1
    t1.add(Task(title="Write tests"))
    assert len(t1) == 2
    
def test_get_by_id_returns_matching_task(populated_list):
    target = populated_list._tasks[0]
    found = populated_list.get_by_id(target.id)
    assert found is target
    
def test_get_by_id_raises_when_not_found(populated_list):
    with pytest.raises(KeyError):
        populated_list.get_by_id("does-not-exist")

def test_complete_marks_task_done():
    pass

def test_remove_deletes_task_from_list():
    task_list = TaskList()

    task = Task(title="Buy milk")

    task_list.add(task)

    task_list.remove(task.id)

    assert len(task_list._tasks) == 0
    
def test_remove_raises_error_if_task_not_found():
    task_list = TaskList()

    with pytest.raises(ValueError):
        task_list.remove("missing-id")    
