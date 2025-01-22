import pytest

from lzqueue import AsyncLocalQueue


@pytest.fixture
async def queue():
    # Create the queue
    q = AsyncLocalQueue(":memory:")
    # Open immediately (optional) or lazily
    await q.ensure_open()

    try:
        # Provide it to your test
        yield q
    finally:
        # Always close, even if test fails
        await q.close()


@pytest.mark.anyio
async def test_async_local_queue_fifo(queue):
    # Enqueue
    await queue.enqueue("hello")
    await queue.enqueue("world")

    # Dequeue
    claimed1 = await queue.dequeue()
    assert claimed1.payload == "hello"
    claimed2 = await queue.dequeue()
    assert claimed2.payload == "world"

    # Nothing left
    none_msg = await queue.dequeue()
    assert none_msg is None

    await queue.close()


@pytest.mark.anyio
async def test_invalid_queue_uri(monkeypatch):
    """
    Test AsyncLocalQueue with invalid URI path.
    """
    # Simulate an invalid environment variable
    monkeypatch.setenv("SQLITE_QUEUE_PATH", "/invalid/path/to/queue.db")
    with pytest.raises(OSError):
        queue = AsyncLocalQueue()
        await queue.ensure_open()


@pytest.mark.anyio
async def test_search_completed_flag(queue):
    """
    Test the 'completed' flag handling in the search method.
    """
    queue = AsyncLocalQueue(":memory:")
    await queue.enqueue("completed-message", max_claims=1)
    message = await queue.dequeue()
    await queue.ack(message.message_id)

    # Search for completed messages
    completed_msgs = await queue.search(completed=True)
    assert len(completed_msgs) == 1
    assert completed_msgs[0].payload == "completed-message"

    # Search for uncompleted messages
    uncompleted_msgs = await queue.search()
    assert len(uncompleted_msgs) == 0

    await queue.close()


@pytest.mark.anyio
async def test_async_local_queue_file(tmp_path):
    """
    Test using a real file path so line 20 is executed:
        uri = str(uri_path)
    """
    db_file = tmp_path / "testdb.sqlite"
    q = AsyncLocalQueue(str(db_file))  # triggers line 20
    await q.ensure_open()
    await q.close()
