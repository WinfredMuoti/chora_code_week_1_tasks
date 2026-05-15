from tasks import TaskList
from tasks import Task

def test_new_list_is_empty():
    t1 = TaskList()
    assert len(t1) == 0
    
def test_add_increases_length():
    t1 = TaskList()
    t1.add(Task(title="Buy milk"))
    assert len(t1) == 1
    t1.add(Task(title="Write tests"))
    assert len(t1) == 2
