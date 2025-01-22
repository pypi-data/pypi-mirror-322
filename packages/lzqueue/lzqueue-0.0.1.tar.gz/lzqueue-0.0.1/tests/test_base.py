from lzqueue.base import Queue


def test_from_uri_http():
    q = Queue.from_uri("http://localhost")
    # That should produce a RemoteClient, verifying line coverage
    from lzqueue.remote.client import RemoteClient

    assert isinstance(q, RemoteClient)


def test_from_uri_local():
    q = Queue.from_uri(":memory:")
    from lzqueue import LocalQueue

    assert isinstance(q, LocalQueue)
