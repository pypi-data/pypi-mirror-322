import json
import sys

import click

from . import AsyncLocalQueue, Queue


def shared_options(f):
    """
    Decorator to share the --uri option across all commands.
    """
    f = click.option(
        "--uri",
        default=None,
        help="Path to local DB or http:// remote URI.",
    )(f)
    return f


@shared_options
@click.pass_context
def _cli(ctx, uri):
    """
    CLI for local or remote queue usage.
    """
    ctx.obj = Queue.from_uri(uri)


cli = click.group(_cli)


@cli.command()
@click.argument("payload", required=False)
@click.pass_context
def push(ctx, payload):
    """
    Push a new message on top of the stack (LIFO).
    """
    if not payload:
        payload = sys.stdin.read().rstrip("\n")
        if not payload:
            click.echo(
                "Error: No payload provided (argument or stdin).",
                err=True,
            )
            ctx.exit(1)

    message = ctx.obj.push(payload)
    if message:
        click.echo(message.model_dump_json().strip())


@cli.command()
@click.pass_context
def peek(ctx):
    """
    Peek at the top of the stack (doesn't claim or complete).
    """
    message = ctx.obj.peek()
    if message:
        click.echo(message.model_dump_json())


@cli.command()
@click.pass_context
def pop(ctx):
    """
    Pop the top message from the stack (claims & completes).
    """
    message = ctx.obj.pop()
    if message:
        click.echo(message.model_dump_json())


@cli.command()
@click.argument("payload", required=False)
@click.option(
    "--topic",
    default=None,
    help="Optional topic label.",
)
@click.option(
    "--for_",
    "--for",
    "for_",
    default=None,
    help="Target queue consumer.",
)
@click.option(
    "--priority",
    default=0,
    type=int,
    help="Priority integer (higher = urgent).",
)
@click.option(
    "--unique_id",
    default=None,
    help="Unique identifier for dedup.",
)
@click.option(
    "--delay",
    default=0,
    type=int,
    help="Seconds to delay before visible.",
)
@click.option(
    "--timeout",
    default=600,
    type=int,
    help="Visibility timeout or reclaim time.",
)
@click.option(
    "--max-claims",
    default=2,
    type=int,
    help="Maximum claims allowed.",
)
@click.pass_context
def enqueue(
    ctx,
    payload,
    topic,
    for_,
    priority,
    unique_id,
    delay,
    timeout,
    max_claims,
):
    """
    Enqueue (FIFO) a message.  Doesn't complete automatically.
    """
    if not payload:
        payload = sys.stdin.read().rstrip("\n")
        if not payload:
            click.echo(
                "Error: No payload provided (argument or stdin).",
                err=True,
            )
            ctx.exit(1)

    message = ctx.obj.enqueue(
        payload,
        topic=topic,
        for_=for_,
        priority=priority,
        unique_id=unique_id,
        delay=delay,
        timeout=timeout,
        max_claims=max_claims,
    )
    if message:
        click.echo(message.model_dump_json().strip())


@cli.command()
@click.option(
    "--topic",
    default=None,
    help="Filter by topic.",
)
@click.option(
    "--for_",
    "--for",
    "for_",
    default=None,
    help="Filter by queued_for.",
)
@click.option(
    "--by",
    default=None,
    help="Specify consumer identity for receiving.",
)
@click.option(
    "--after",
    default=None,
    type=int,
    help="Minimum 'added_at' time.",
)
@click.option(
    "--before",
    default=None,
    type=int,
    help="Maximum 'added_at' time.",
)
@click.option(
    "--no-ack",
    is_flag=True,
    default=False,
    help="Immediately complete the message.",
)
@click.pass_context
def dequeue(ctx, topic, for_, by, after, before, no_ack):
    """
    Dequeue (FIFO) the oldest message
    """
    message = ctx.obj.dequeue(
        topic=topic,
        for_=for_,
        by=by,
        after=after,
        before=before,
        no_ack=no_ack,
    )
    if message:
        click.echo(message.model_dump_json())


@cli.command()
@click.argument("message_id", required=True, type=int)
@click.pass_context
def ack(ctx, message_id):
    """
    Acknowledge (complete) a claimed message by ID.
    """
    message = ctx.obj.ack(message_id)
    if message:
        click.echo(message.model_dump_json())


@cli.command()
@click.option(
    "--topic",
    default=None,
    help="Filter by topic.",
)
@click.option(
    "--for_",
    "--for",
    "for_",
    default=None,
    help="Filter by queued_for.",
)
@click.option(
    "--by",
    default=None,
    help="Filter by consumer identity.",
)
@click.option(
    "--after",
    default=None,
    type=int,
    help="Minimum 'added_at' or 'claimed_at'.",
)
@click.option(
    "--before",
    default=None,
    type=float,
    help="Maximum 'added_at' or 'claimed_at'.",
)
@click.pass_context
def front(ctx, topic, for_, by, after, before):
    """
    View the oldest unclaimed message (front of the FIFO queue).
    """
    message = ctx.obj.front(
        topic=topic,
        for_=for_,
        by=by,
        after=after,
        before=before,
    )
    if message:
        click.echo(message.model_dump_json())


@cli.command()
@click.option("--topic", default=None)
@click.option("--for_", "--for", "for_", default=None)
@click.option("--by", default=None)
@click.option("--after", default=None, type=float)
@click.option("--before", default=None, type=float)
@click.pass_context
def back(ctx, topic, for_, by, after, before):
    """
    View the newest unclaimed message (back of the FIFO queue).
    """
    message = ctx.obj.back(
        topic=topic,
        for_=for_,
        by=by,
        after=after,
        before=before,
    )
    if message:
        click.echo(message.model_dump_json())


@cli.command()
@click.pass_context
def status(ctx):
    """
    Show total, unclaimed, and completed message counts.
    """
    st = ctx.obj.status()
    click.echo(json.dumps(st))


@cli.command()
@click.option(
    "--before",
    type=float,
    required=True,
    help="Delete messages older than this 'added_at' timestamp.",
)
@click.pass_context
def delete(ctx, before):
    """
    Delete messages older than a certain time (added_at <= before).
    """
    count = ctx.obj.delete(before=before)
    click.echo(f"Deleted {count} messages.")


@cli.command()
@click.option(
    "--topic",
    default=None,
    help="Filter by topic.",
)
@click.option(
    "--for_",
    "--for",
    "for_",
    default=None,
    help="Filter by queued_for.",
)
@click.option(
    "--by",
    default=None,
    help="Filter by consumer.",
)
@click.option(
    "--after",
    default=None,
    type=float,
    help="Minimum added_at.",
)
@click.option(
    "--before",
    default=None,
    type=float,
    help="Maximum added_at.",
)
@click.option(
    "--claimed",
    is_flag=True,
    default=False,
    help="Search only claimed messages.",
)
@click.option(
    "--completed",
    is_flag=True,
    default=False,
    help="Search only completed messages.",
)
@click.option(
    "--dead",
    is_flag=True,
    default=False,
    help="Search only dead messages.",
)
@click.option(
    "--limit",
    default=10,
    type=int,
    help="Max rows to return.",
)
@click.pass_context
def search(ctx, topic, for_, by, after, before, claimed, completed, dead, limit):
    """
    Search messages using filters
    """
    results = ctx.obj.search(
        topic=topic,
        for_=for_,
        by=by,
        after=after,
        before=before,
        claimed=claimed,
        completed=completed,
        dead=dead,
        limit=limit,
    )
    for msg in results or []:
        click.echo(msg.model_dump_json())


@cli.command()
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=8000, type=int)
@click.pass_context
def serve(ctx, host, port):  # pragma: no cover
    """Start REST API queue server"""
    import uvicorn

    from .remote.server import app, set_queue

    async_queue = AsyncLocalQueue(ctx.obj.uri)
    set_queue(async_queue)
    uvicorn.run(app, host=host, port=port)
