import time

from lzqueue import LocalQueue


def test_filtered_searches():
    """
    Test that 'search()' properly excludes dead messages unless dead=True.
    """
    queue = LocalQueue(":memory:")
    timeout = 0.01

    m = [
        queue.enqueue("normal", max_claims=2, timeout=timeout),
        queue.enqueue("with-timeout", max_claims=1, timeout=timeout),
        queue.enqueue("no-timeout", max_claims=1, timeout=0.0),
    ]

    assert len(queue.search()) == 3

    assert queue.dequeue() == m[0]
    assert len(queue.search()) == 2
    assert len(queue.search(claimed=True)) == 1

    assert queue.dequeue() == m[1]
    assert len(queue.search()) == 1
    assert len(queue.search(claimed=True)) == 2
    assert len(queue.search(dead=True)) == 0

    assert queue.dequeue() == m[2]
    assert len(queue.search()) == 0
    assert len(queue.search(claimed=True)) == 2
    assert len(queue.search(dead=True)) == 1  # message 3 is DOA

    assert queue.dequeue() is None

    time.sleep(timeout)
    assert len(queue.search()) == 1  # message 1 timed out, but not dead
    assert len(queue.search(claimed=True)) == 0
    assert len(queue.search(dead=True)) == 2  # message 2 timed out.
