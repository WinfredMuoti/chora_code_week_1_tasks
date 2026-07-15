from tasks import Task


def test_task_has_title_and_starts_not_done():
    task = Task(title="Buy milk", user_id="user-1")
    assert task.title == "Buy milk"
    assert task.done is False


def test_each_task_has_unique_id():
    t1 = Task(title="A", user_id="user-1")
    t2 = Task(title="A", user_id="user-1")
    assert t1.id != t2.id


def test_mark_done_sets_done_to_true():
    task = Task(title="X", user_id="user-1")
    assert task.done is False
    task.mark_done()
    assert task.done is True
