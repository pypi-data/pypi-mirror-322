from abc import ABC, abstractmethod
from enum import Enum
from time import time
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, computed_field

ViewType = Literal["front", "back", "claimed", "completed"]
SQLITE_QUEUE_PATH = "~/.sqlite_queue.db"


class MessageStatus(Enum):
    QUEUED = "queued"
    CLAIMED = "claimed"
    COMPLETED = "completed"
    DEAD = "dead"


class Message(BaseModel):
    message_id: int = Field(...)
    unique_id: Optional[str] = None
    priority: int = Field(default=0)
    topic: Optional[str] = None
    payload: str
    timeout: float = Field(default=600.0)
    claims: int = Field(default=0)
    max_claims: int = Field(default=2)
    delay: float = Field(default=0.0)
    queued_for: Optional[str] = None
    received_by: Optional[str] = None
    added_at: float = Field(...)
    claimed_at: float = Field(default=0.0)
    completed_at: float = Field(default=0.0)

    def __eq__(self, other):
        # check the immutable fields only
        # skip claimed_at, completed_at, received_by, and claims
        return (
            self.added_at == other.added_at
            and self.delay == other.delay
            and self.max_claims == other.max_claims
            and self.message_id == other.message_id
            and self.payload == other.payload
            and self.priority == other.priority
            and self.queued_for == other.queued_for
            and self.timeout == other.timeout
            and self.topic == other.topic
            and self.unique_id == other.unique_id
        )

    @computed_field
    @property
    def status(self) -> MessageStatus:
        """
        Determine the message's current state based on completed_at,
        claims, claimed_at, and timeout, using an if-elif-else chain.
        """

        now = time()

        is_completed = self.completed_at > 0
        is_claimed = self.claimed_at > 0
        is_timed_out = ((self.claimed_at + self.timeout) < now) and is_claimed
        is_out_of_claims = self.claims >= self.max_claims

        if is_completed:
            return MessageStatus.COMPLETED

        if is_claimed:
            # If it's timed out...
            if is_timed_out:
                # ...and out of claims => DEAD
                if is_out_of_claims:
                    return MessageStatus.DEAD
                else:
                    # timed out but still has claims => "QUEUED"
                    return MessageStatus.QUEUED
            else:
                # claimed but not timed out => "CLAIMED"
                return MessageStatus.CLAIMED

        # If never claimed => "QUEUED"
        return MessageStatus.QUEUED


class Queue(ABC):
    @abstractmethod
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
        """
        Enqueue or push a new message into the queue.
        Returns None if the message unique_id is a duplicate.
        """

    @abstractmethod
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
        """
        Claim the oldest unclaimed & uncompleted message.
        If no_ack is True, sets completed_at immediately.
        Returns the claimed message row or None if empty.
        """

    @abstractmethod
    def ack(self, message_id: int) -> Message | None:
        """
        Mark a claimed message as completed.
        """

    @abstractmethod
    def push(self, payload: str) -> Message | None:
        """
        Push a new message onto the top of the queue.
        Returns None if the message unique_id is a duplicate.
        """

    @abstractmethod
    def pop(self, by: Optional[str] = None) -> Message | None:
        """
        Claims and completes the message in a single operation.
        """

    @abstractmethod
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
        """
        View Message at front or back, or most recent claimed or completed.
        """

    def front(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> Message | None:
        return self.view(
            "front",
            topic=topic,
            for_=for_,
            by=by,
            after=after,
            before=before,
        )

    def back(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> Message | None:
        return self.view(
            "back",
            topic=topic,
            for_=for_,
            by=by,
            after=after,
            before=before,
        )

    def claimed(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> Message | None:
        return self.view(
            "claimed",
            topic=topic,
            for_=for_,
            by=by,
            after=after,
            before=before,
        )

    def completed(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> Message | None:
        return self.view(
            "completed",
            topic=topic,
            for_=for_,
            by=by,
            after=after,
            before=before,
        )

    @abstractmethod
    def status(self) -> dict[str, Any]:
        """
        Return a quick snapshot of queue counts, etc.
        """

    @abstractmethod
    def delete(self, *, before: float = 0.0) -> int:
        """
        Example: delete messages older than a timestamp.
        Returns the number of rows deleted.
        """

    @abstractmethod
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
        """
        Find messages filtered by fields.
        """

    @classmethod
    def from_uri(cls, uri: Optional[str] = None) -> "Queue":
        if uri is not None and uri.startswith("http"):
            from .remote.client import RemoteClient

            return RemoteClient(uri)

        else:
            from . import LocalQueue

            return LocalQueue(uri=uri)
