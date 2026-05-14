from tasks import Tasklist

def test_new_list_is_empty():
    t1 = Tasklist()
    assert len(t1) == 0