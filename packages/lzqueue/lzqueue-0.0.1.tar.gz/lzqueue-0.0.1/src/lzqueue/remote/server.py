from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .. import AsyncLocalQueue, Message
from . import models

queue: AsyncLocalQueue


def set_queue(_queue: AsyncLocalQueue):
    """Allow the LocalQueue to be set by CLI."""
    global queue
    queue = _queue


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Lifecycle manager for FastAPI app."""
    # Initialize on startup
    global queue

    if queue is None:
        queue = AsyncLocalQueue()

    await queue.ensure_open()

    # Yield Control to FastAPI server
    yield


app = FastAPI(title="LocalQueue API")


@app.post("/")
async def root():
    return await queue.status()


@app.post("/enqueue")
async def enqueue(item: models.EnqueueItem) -> Message:
    message = await queue.enqueue(**item.model_dump())
    if message is None:
        raise HTTPException(status_code=409, detail="duplicate unique_id")
    return message


@app.post("/dequeue")
async def dequeue(item: models.DequeueItem) -> Message | None:
    return await queue.dequeue(**item.model_dump())


@app.post("/ack")
async def ack(item: models.AckItem) -> Message | None:
    return await queue.ack(item.message_id)


@app.post("/push")
async def push(params: models.PushItem) -> Message | None:
    return await queue.push(payload=params.payload)


@app.post("/pop")
async def pop(item: models.PopItem) -> Message | None:
    return await queue.pop(**item.model_dump())


@app.post("/view")
async def view(item: models.ViewItem) -> Message | None:
    return await queue.view(**item.model_dump())


@app.post("/delete")
async def delete(item: models.DeleteItem) -> int:
    return await queue.delete(**item.model_dump())


@app.post("/search")
async def search(item: models.SearchItem) -> list[Message]:
    results = await queue.search(**item.model_dump())
    return results
