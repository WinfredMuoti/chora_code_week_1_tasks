from tasks import Task
 
def test_task_has_title_and_starts_not_done():
    task = Task(title="Buy milk")
    assert task.title == "Buy milk"
    assert task.done is False