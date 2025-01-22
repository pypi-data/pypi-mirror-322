import time
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

from lzqueue import AsyncLocalQueue, LocalQueue, Message, MessageStatus, Queue
from lzqueue.remote.client import RemoteClient
from lzqueue.remote.server import app, set_queue


@pytest.fixture
async def q(request, anyio_backend) -> AsyncGenerator[Queue, None]:
    """
    Parametrized fixture for local and remote testing.
    """
    mode = request.param
    if mode == "local":
        yield LocalQueue(uri=":memory:")

    elif mode == "remote":
        async_local = AsyncLocalQueue(":memory:")
        set_queue(async_local)
        client = TestClient(app)
        try:
            yield RemoteClient(client=client)
        finally:
            await async_local.close()  # must be awaited


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_enqueue_claim_delete(q: Queue):
    pushed = q.enqueue("hello claim-delete")
    assert isinstance(pushed, Message)
    assert pushed.message_id == 1
    assert pushed.payload == "hello claim-delete"
    assert pushed.completed_at == 0
    assert pushed.claimed_at == 0
    assert pushed.added_at > 0

    claimed = q.dequeue()
    assert claimed is not None
    assert claimed.message_id == pushed.message_id == 1
    assert claimed.claimed_at > 0
    assert claimed.completed_at == 0
    assert claimed.added_at == pushed.added_at

    completed = q.ack(claimed.message_id)
    assert completed is not None
    assert completed.message_id == pushed.message_id == 1
    assert completed.claimed_at == claimed.claimed_at
    assert completed.completed_at > 0
    assert completed.added_at == pushed.added_at

    # nothing left
    assert q.dequeue() is None


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_pop_fifo(q: Queue):
    m1 = q.push("first")
    m2 = q.push("second")
    m3 = q.push("third")
    assert m1 and m2 and m3

    p1 = q.pop()
    assert p1 is not None
    assert p1.message_id == m3.message_id
    assert p1.payload == "third"

    p2 = q.pop()
    assert p2 is not None
    assert p2.message_id == m2.message_id
    assert p2.payload == "second"

    p3 = q.pop()
    assert p3 is not None
    assert p3.message_id == m1.message_id
    assert p3.payload == "first"

    # no more
    assert q.pop() is None


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_status(q: Queue):
    assert q.status() == {"completed": 0, "total": 0, "unclaimed": 0}


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_view_and_search(q: Queue):
    # Enqueue a few messages
    m1 = q.enqueue("apple", topic="fruit")
    m2 = q.enqueue("banana", topic="fruit")
    m3 = q.enqueue("carrot", topic="veggie")

    # front() -> oldest unclaimed & uncompleted
    assert q.front(topic="fruit") == m1
    assert q.front(topic="veggie") == m3

    # back() -> newest unclaimed & uncompleted
    assert q.back(topic="fruit") == m2

    # claim/dequeue veggie
    assert q.dequeue(topic="veggie") == m3
    assert q.view("front", topic="veggie") is None
    assert q.claimed() == m3

    # complete it
    assert q.ack(m3.message_id).completed_at > 0

    # "completed" view type
    assert q.claimed() is None
    assert q.completed() == m3

    # Search queued messages
    assert len(q.search(topic="fruit")) == 2
    assert len(q.search(topic="veggie")) == 0
    assert len(q.search(topic="veggie", completed=True)) == 1

    # Test Delete
    assert q.delete(before=time.time()) == 3
    assert q.status() == {"completed": 0, "total": 0, "unclaimed": 0}


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_dead_messages(q: Queue):
    # Enqueue with max_claims=1
    msg_1 = q.enqueue("one-try-only", max_claims=1, timeout=0.0)
    msg_2 = q.enqueue("two-try-only", max_claims=2, timeout=0.0)

    first = q.dequeue()
    assert first.message_id == msg_1.message_id

    second = q.dequeue()
    assert second.message_id == msg_2.message_id
    assert second.claims == 1

    time.sleep(0.01)
    third = q.dequeue()
    assert third.message_id == msg_2.message_id
    assert third.claims == 2

    assert q.dequeue() is None


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_priority_queue(q: Queue):
    q.enqueue("low priority", priority=1)
    q.enqueue("high priority", priority=10)

    # Dequeue => expecting "high priority" first
    first = q.dequeue()
    assert first is not None
    assert first.payload == "high priority"

    # Next => "low priority"
    second = q.dequeue()
    assert second is not None
    assert second.payload == "low priority"


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_delay_availability(q: Queue):
    # 10ms delay (increase if flaky)
    delay = 0.05

    # Enqueue two messages
    q.enqueue("delayed", delay=delay)
    q.enqueue("immediate", delay=0.0)

    # Immediately attempt to dequeue => get "immediate"
    first = q.dequeue()
    assert first and first.payload == "immediate"

    # Next => should be None (no item available)
    second = q.dequeue()
    assert second is None

    # Sleep => "delayed" should be available
    time.sleep(delay)
    third = q.dequeue()
    assert third and third.payload == "delayed"


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_unique_id_no_dupes(q: Queue):
    uid = "ABC"
    assert q.enqueue("first", unique_id=uid).unique_id == uid
    assert q.enqueue("second", unique_id=uid) is None

    assert q.dequeue().payload == "first"
    assert q.dequeue() is None

    # even after dequeue, unique_id still prevents dupes
    assert q.enqueue("second", unique_id=uid) is None


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_timeout_reclaim(q: Queue):
    # 10ms delay (increase if flaky)
    timeout = 0.01

    msg_1 = q.enqueue("timeout test", timeout=timeout)
    assert msg_1

    first_claim = q.dequeue()
    assert first_claim is not None
    assert first_claim.message_id == msg_1.message_id

    # Immediately => nothing left
    assert q.dequeue() is None

    # wait
    time.sleep(timeout * 1.1)

    # Now the message should be available again
    second_claim = q.dequeue()
    assert second_claim is not None
    assert second_claim.message_id == msg_1.message_id


@pytest.mark.parametrize("q", ["local", "remote"], indirect=True)
async def test_max_claims(q: Queue):
    timeout = 0.001

    msg = q.enqueue("max claims test", max_claims=2, timeout=timeout)

    # claim 1
    assert q.dequeue(no_ack=False).message_id == msg.message_id

    # let it time out
    time.sleep(timeout * 1.1)
    assert q.dequeue(no_ack=False).message_id == msg.message_id

    # let it time out again
    time.sleep(timeout * 1.1)
    assert q.dequeue() is None, "Exceeded max_claims=2"


def test_message_status():
    # 1) COMPLETED
    msg_completed = Message(
        message_id=1,
        completed_at=100.0,  # Anything > 0
        claimed_at=0.0,
        claims=0,
        max_claims=1,
        timeout=10,
        payload="completed-test",
        added_at=0.0,
    )
    assert msg_completed.status == MessageStatus.COMPLETED

    # 2) CLAIMED (claimed but not timed out, not completed)
    now = time.time()
    msg_claimed = Message(
        message_id=2,
        completed_at=0.0,
        claimed_at=now,  # has been claimed
        claims=1,
        max_claims=3,
        timeout=600.0,  # well into the future
        payload="claimed-test",
        added_at=now - 1,
    )
    assert msg_claimed.status == MessageStatus.CLAIMED

    # 3) DEAD (claimed, timed out, out_of_claims)
    msg_dead = Message(
        message_id=3,
        completed_at=0.0,
        claimed_at=now - 1000,  # definitely timed out
        claims=2,
        max_claims=2,  # out_of_claims
        timeout=10.0,
        payload="dead-test",
        added_at=now - 1000,
    )
    assert msg_dead.status == MessageStatus.DEAD

    # 4) QUEUED (never claimed, not completed)
    msg_queued = Message(
        message_id=4,
        completed_at=0.0,
        claimed_at=0.0,  # never claimed
        claims=0,
        max_claims=2,
        timeout=10.0,
        payload="queued-test",
        added_at=now,
    )
    assert msg_queued.status == MessageStatus.QUEUED

    # 5) Timed out but NOT out_of_claims => "QUEUED"
    msg_timed_out_but_claims_left = Message(
        message_id=5,
        completed_at=0.0,
        claimed_at=now - 1000,  # definitely timed out
        claims=1,
        max_claims=2,  # still has claims left
        timeout=10.0,
        payload="timeout-but-queued",
        added_at=now - 1000,
    )
    assert msg_timed_out_but_claims_left.status == MessageStatus.QUEUED
