from tasks import Task
 
def test_task_has_title_and_starts_not_done():
    task = Task(title="Buy milk")
    assert task.title == "Buy milk"
    assert task.done is False
    
def test_each_task_has_unique_id():
    t1 = Task(title="A")
    t2 = Task(title="A")
    assert t1.id != t2.id    
    
    