from typing import Any, Optional

from .. import Message, Queue, ViewType


class RemoteClient(Queue):
    """
    A client that talks to the FastAPI-based queue server.
    """

    def __init__(
        self,
        uri: str | None = None,
        client=None,
    ):  # pragma: no cover
        if uri and not client:
            import httpx

            self.client = httpx.Client(base_url=uri.rstrip("/"))
        elif client:
            self.client = client
        elif not uri:
            raise ValueError("Invalid uri: {uri}")

    def call(self, path, data=None, as_message=True) -> Any:
        response = self.client.post(path, json=data or {})

        # 409: Duplicate unique_id
        if response.status_code != 409:
            response.raise_for_status()
            data = response.json()
            return Message(**data) if as_message and data else data

    def enqueue(
        self,
        payload: str,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        priority: int = 0,
        unique_id: Optional[str] = None,
        delay: float = 0.0,
        timeout: float = 600.0,
        max_claims: int = 2,
    ) -> Message | None:
        return self.call(
            "/enqueue",
            {
                "payload": payload,
                "topic": topic,
                "for": for_,
                "priority": priority,
                "unique_id": unique_id,
                "delay": delay,
                "timeout": timeout,
                "max_claims": max_claims,
            },
        )

    def dequeue(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
        no_ack: bool = False,
    ) -> Message | None:
        return self.call(
            "/dequeue",
            {
                "topic": topic,
                "for": for_,
                "by": by,
                "after": after,
                "before": before,
                "no_ack": no_ack,
            },
        )

    def ack(self, message_id: int) -> Message | None:
        return self.call("/ack", {"message_id": message_id})

    def push(self, payload: str) -> Message | None:
        return self.call(
            "/push",
            {
                "payload": payload,
            },
        )

    def pop(self, by: Optional[str] = None) -> Message | None:
        return self.call(
            "/pop",
            {
                "by": by,
            },
        )

    def view(
        self,
        view_type: ViewType = "front",
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> Message | None:
        return self.call(
            "/view",
            {
                "view_type": view_type,
                "topic": topic,
                "for": for_,
                "by": by,
                "after": after,
                "before": before,
            },
        )

    def status(self) -> dict[str, Any]:
        return self.call("/", as_message=False)

    def delete(self, *, before: float = 0.0) -> int:
        return self.call(
            "/delete",
            {
                "before": before,
            },
            as_message=False,
        )

    def search(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
        claimed: bool = False,
        completed: bool = False,
        dead: bool = False,
        limit: int = 10,
    ) -> list[Message]:
        rows = self.call(
            "/search",
            {
                "after": after,
                "before": before,
                "by": by,
                "claimed": claimed,
                "completed": completed,
                "dead": dead,
                "for": for_,
                "limit": limit,
                "topic": topic,
            },
            as_message=False,
        )
        return [Message(**row) for row in rows]
