import os
import pathlib
from typing import Any, Optional

import aiosqlite

from . import SQLITE_QUEUE_PATH, Message, ViewType, sql


class AsyncLocalQueue:
    def __init__(self, uri: Optional[str] = None):
        if not uri:
            uri = os.environ.get("SQLITE_QUEUE_PATH", "").strip()
            uri = uri or SQLITE_QUEUE_PATH

        if ":memory:" not in uri:
            uri_path = pathlib.Path(uri).resolve().absolute()
            uri_path.parent.mkdir(parents=True, exist_ok=True)
            uri = str(uri_path)

        self.uri = uri
        self._conn: aiosqlite.Connection | None = None

    async def ensure_open(self) -> aiosqlite.Connection:
        """Open the DB if not open yet. Equivalent to lazy init."""
        if self._conn is None:
            _conn = await aiosqlite.connect(self.uri)
            _conn.row_factory = aiosqlite.Row

            await _conn.execute(sql.CREATE_TABLE)
            for indexes in sql.CREATE_INDEXES:
                await _conn.execute(indexes)
            await _conn.commit()

            self._conn = _conn

        return self._conn

    async def close(self):
        """Close the aiosqlite connection if open."""
        if self._conn:
            await self._conn.close()
            self._conn = None

    # -------------------------------------------------
    # Overriding the abstract methods from base.Queue
    # -------------------------------------------------

    async def enqueue(
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
        conn = await self.ensure_open()
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
            async with conn.execute(sql.INSERT_MESSAGE, params) as cur:
                row = await cur.fetchone()
                await conn.commit()
                if row is not None:
                    message = Message(**row)

        except aiosqlite.IntegrityError:
            pass

        return message

    async def dequeue(
        self,
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
        no_ack: bool = False,
    ) -> Message | None:
        conn = await self.ensure_open()
        params = {
            "topic": topic,
            "for": for_,
            "by": by,
            "after": after,
            "before": before,
            "no_ack": int(no_ack),
        }
        async with conn.execute(sql.DEQUEUE_MESSAGE, params) as cur:
            row = await cur.fetchone()
        await conn.commit()
        return Message(**row) if row else None

    async def ack(self, message_id: int) -> Message | None:
        conn = await self.ensure_open()
        params = {"message_id": message_id}
        async with conn.execute(sql.ACK_MESSAGE, params) as cur:
            row = await cur.fetchone()
        await conn.commit()
        return Message(**row) if row else None

    async def push(self, payload: str) -> Message | None:
        return await self.enqueue(payload)

    async def pop(self, by: Optional[str] = None) -> Message | None:
        conn = await self.ensure_open()
        async with conn.execute(sql.POP_MESSAGE_LIFO, {"by": by}) as cur:
            row = await cur.fetchone()
        await conn.commit()
        return Message(**row) if row else None

    async def view(
        self,
        view_type: ViewType = "front",
        *,
        topic: Optional[str] = None,
        for_: Optional[str] = None,
        by: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> Message | None:
        conn = await self.ensure_open()
        sql_map = {
            "front": sql.FRONT_MESSAGE,
            "back": sql.BACK_MESSAGE,
            "claimed": sql.CLAIMED_MESSAGE,
            "completed": sql.COMPLETED_MESSAGE,
        }
        sql_query = sql_map.get(view_type, sql.FRONT_MESSAGE)
        params = {
            "topic": topic,
            "for": for_,
            "by": by,
            "after": after,
            "before": before,
        }
        async with conn.execute(sql_query, params) as cur:
            row = await cur.fetchone()
        return Message(**row) if row else None

    async def status(self) -> dict[str, Any] | None:
        conn = await self.ensure_open()
        async with conn.execute(sql.STATUS_QUERY) as cur:
            row = await cur.fetchone()

        return (
            {
                "total": row["total"],
                "unclaimed": row["unclaimed"],
                "completed": row["completed"],
            }
            if row is not None
            else None
        )

    async def delete(self, *, before: float = 0.0) -> int:
        conn = await self.ensure_open()
        async with conn.execute(sql.DELETE_BEFORE, {"before": before}) as cur:
            await conn.commit()
            return cur.rowcount

    async def search(
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
        conn = await self.ensure_open()

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
        async with conn.execute(sql.SEARCH_MESSAGES, params) as cur:
            rows = await cur.fetchall()
        return [Message(**row) for row in rows]
