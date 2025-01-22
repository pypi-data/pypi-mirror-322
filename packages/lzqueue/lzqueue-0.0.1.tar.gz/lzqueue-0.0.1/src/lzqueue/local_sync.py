import os
import pathlib
import sqlite3
from typing import Any, Optional

from . import SQLITE_QUEUE_PATH, Message, Queue, ViewType, sql


class LocalQueue(Queue):
    """
    LocalQueue is a minimal example of a queue-like interface on top
    of SQLite. You can expand or reorganize to match your project's needs.
    """

    def __init__(self, uri: Optional[str] = None):
        """
        :param uri: Path to the SQLite database or ":memory:".
                    Defaults to the environment variable
                    SQLITE_QUEUE_PATH if not provided.
        """

        uri = uri or os.environ.get("SQLITE_QUEUE_PATH") or SQLITE_QUEUE_PATH
        uri = uri.strip()

        # Create directories if it's a file path and not in-memory.
        if ":memory:" not in uri:
            uri_path = pathlib.Path(uri).expanduser().resolve().absolute()
            uri_path.parent.mkdir(parents=True, exist_ok=True)
            uri = str(uri_path)

        self.uri = uri
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            conn = sqlite3.connect(
                self.uri,
                isolation_level=None,  # autocommit mode
                check_same_thread=False,  # allow usage across threads
            )
            conn.row_factory = sqlite3.Row

            conn.execute(sql.CREATE_TABLE)
            for create_index in sql.CREATE_INDEXES:
                conn.execute(create_index)
            conn.commit()

            self._conn = conn
        return self._conn

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
        params = {
            "payload": payload,
            "topic": topic,
            "for": for_,
            "priority": priority,
            "unique_id": unique_id,
            "delay": delay,
            "timeout": timeout,
            "max_claims": max_claims,
        }

        message: Message | None = None

        try:
            cur = self.conn.execute(sql.INSERT_MESSAGE, params)
            row = cur.fetchone()
            message = Message(**row)
        except sqlite3.IntegrityError:
            pass

        return message

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
        params = {
            "topic": topic,
            "for": for_,
            "by": by,
            "after": after,
            "before": before,
            "no_ack": int(no_ack),
        }
        cur = self.conn.execute(sql.DEQUEUE_MESSAGE, params)
        row = cur.fetchone()
        return Message(**row) if row else None

    def ack(self, message_id: int) -> Message | None:
        """
        Mark a claimed message as completed.
        """
        cur = self.conn.execute(sql.ACK_MESSAGE, {"message_id": message_id})
        row = cur.fetchone()
        return Message(**row) if row else None

    def push(self, payload: str) -> Message | None:
        """
        Pushes a new message onto the top of the stack.
        Returns None if the message unique_id is a duplicate.
        """
        return self.enqueue(payload)

    def pop(self, by: Optional[str] = None) -> Message | None:
        """
        Pop the top message off the stack.
        """
        cur = self.conn.execute(sql.POP_MESSAGE_LIFO, {"by": by})
        row = cur.fetchone()
        return Message(**row) if row else None

    def peek(self) -> Message | None:
        """
        Peek at the top message on the stack.
        """
        return self.view("back")

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
        params = {
            "topic": topic,
            "for": for_,
            "by": by,
            "after": after,
            "before": before,
        }

        sql_query = {
            "front": sql.FRONT_MESSAGE,
            "back": sql.BACK_MESSAGE,
            "claimed": sql.CLAIMED_MESSAGE,
            "completed": sql.COMPLETED_MESSAGE,
        }[view_type]

        cur = self.conn.execute(sql_query, params)
        row = cur.fetchone()
        return Message(**row) if row else None

    def status(self) -> dict[str, Any]:
        """
        Return a quick snapshot of queue counts, etc.
        """
        row = self.conn.execute(sql.STATUS_QUERY).fetchone()
        return {
            "total": row["total"],
            "unclaimed": row["unclaimed"],
            "completed": row["completed"],
        }

    def delete(self, *, before: float = 0.0) -> int:
        """
        Example: delete messages older than a timestamp.
        Returns the number of rows deleted.
        """
        cur = self.conn.execute(sql.DELETE_BEFORE, {"before": before})
        return cur.rowcount

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
        Find messages by fields.
        Using the NULL-check approach in SEARCH_MESSAGES.
        """

        # noinspection DuplicatedCode
        queued = not (claimed or completed or dead)
        params = {
            "topic": topic,
            "for": for_,
            "by": by,
            "after": after,
            "before": before,
            "claimed": int(claimed),
            "completed": int(completed),
            "dead": int(dead),
            "queued": int(queued),
            "limit": limit,
        }

        cur = self.conn.execute(sql.SEARCH_MESSAGES, params)
        rows = cur.fetchall()
        return [Message(**row) for row in rows]
