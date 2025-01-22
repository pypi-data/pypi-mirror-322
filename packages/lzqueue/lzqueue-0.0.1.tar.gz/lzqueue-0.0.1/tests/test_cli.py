import json
import pathlib
import tempfile

import pytest
from click.testing import CliRunner

from lzqueue.cli import cli


@pytest.fixture()
def tmp_uri():
    """
    Creates a temporary directory and returns a path-based SQLite URI.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = pathlib.Path(tmpdir) / "queue.db"
        yield str(db_path)
        # After yield, the tempdir is removed automatically.


def test_push_pop(tmp_uri):
    """
    Test push/pop using the CLI with a local sqlite file.
    """
    runner = CliRunner()
    # push
    result = runner.invoke(cli, ["--uri", tmp_uri, "push", "Hello-World"])
    assert result.exit_code == 0

    # peek
    result = runner.invoke(cli, ["--uri", tmp_uri, "peek"])
    assert result.exit_code == 0
    assert "Hello-World" in result.output

    # pop
    result = runner.invoke(cli, ["--uri", tmp_uri, "pop"])
    assert result.exit_code == 0
    assert "Hello-World" in result.output

    # pop again -> no message
    result = runner.invoke(cli, ["--uri", tmp_uri, "pop"])
    assert result.exit_code == 0
    assert result.output.strip() == ""


def test_enqueue_dequeue(tmp_uri):
    """
    Test enqueue/dequeue in FIFO manner, plus ack.
    """
    runner = CliRunner()

    # enqueue 2 messages
    runner.invoke(cli, ["--uri", tmp_uri, "enqueue", "M1", "--topic", "foo"])
    runner.invoke(cli, ["--uri", tmp_uri, "enqueue", "M2", "--topic", "foo"])

    # front => should see M1
    result = runner.invoke(cli, ["--uri", tmp_uri, "front", "--topic", "foo"])
    assert "M1" in result.output

    # back => should see M2
    result = runner.invoke(cli, ["--uri", tmp_uri, "back", "--topic", "foo"])
    assert "M2" in result.output

    # dequeue => claims M1
    result = runner.invoke(cli, ["--uri", tmp_uri, "dequeue", "--topic", "foo"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["payload"] == "M1"

    # ack => completes M1
    msg_id = data["message_id"]
    result = runner.invoke(cli, ["--uri", tmp_uri, "ack", str(msg_id)])
    data_ack = json.loads(result.output)
    assert data_ack["completed_at"] > 0

    # search => only M2 should appear
    result = runner.invoke(cli, ["--uri", tmp_uri, "search", "--topic", "foo"])
    outputs = result.output.strip().split("\n")
    assert len(outputs) == 1
    data_m2 = json.loads(outputs[0])
    assert data_m2["payload"] == "M2"


def test_delete(tmp_uri):
    """
    Test the delete command by 'before' timestamp.
    """
    runner = CliRunner()
    # enqueue two
    runner.invoke(cli, ["--uri", tmp_uri, "enqueue", "Old", "--topic", "time"])
    result = runner.invoke(cli, ["--uri", tmp_uri, "enqueue", "New", "--topic", "time"])
    new_id = json.loads(result.output)["message_id"]

    # figure out the older message's "added_at"
    # Typically you'd 'search' or do 'front'. We'll just do:
    result = runner.invoke(cli, ["--uri", tmp_uri, "search", "--topic", "time"])
    lines = result.output.strip().split("\n")
    # lines => 2 JSON lines
    items = [json.loads(line) for line in lines]
    new_obj = items[0] if items[0]["message_id"] == new_id else items[1]

    # now delete everything older than new_obj["added_at"]
    # which should remove the old message only
    before_val = new_obj["added_at"] - 0.001
    del_result = runner.invoke(cli, ["--uri", tmp_uri, "delete", "--before", str(before_val)])
    assert "Deleted 1 messages." in del_result.output

    # now check search => we should only see the "New" message
    srch = runner.invoke(cli, ["--uri", tmp_uri, "search", "--topic", "time"])
    remaining_lines = srch.output.strip().split("\n")
    assert len(remaining_lines) == 1
    data_new = json.loads(remaining_lines[0])
    assert data_new["message_id"] == new_id


def test_status(tmp_uri):
    runner = CliRunner()
    # status => initially 0
    result = runner.invoke(cli, ["--uri", tmp_uri, "status"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["completed"] == 0
    assert data["total"] == 0
    assert data["unclaimed"] == 0

    # push
    runner.invoke(cli, ["--uri", tmp_uri, "push", "One"])
    # status => total=1, unclaimed=1, completed=0
    result = runner.invoke(cli, ["--uri", tmp_uri, "status"])
    data = json.loads(result.output)
    assert data["completed"] == 0
    assert data["total"] == 1
    assert data["unclaimed"] == 1


def test_push_stdin(tmp_uri):
    """
    Test 'push' command with payload from stdin.
    """
    runner = CliRunner()
    # Provide stdin input via the 'input' parameter
    result = runner.invoke(cli, ["--uri", tmp_uri, "push"], input="input-from-stdin\n")
    assert result.exit_code == 0, f"Error: {result.output}"
    assert "input-from-stdin" in result.output

    # Verify the message was pushed
    peek_result = runner.invoke(cli, ["--uri", tmp_uri, "peek"])
    assert peek_result.exit_code == 0
    assert "input-from-stdin" in peek_result.output


def test_enqueue_stdin(tmp_uri):
    """
    Test 'enqueue' command with payload from stdin.
    """
    runner = CliRunner()
    # Provide stdin input via the 'input' parameter
    result = runner.invoke(
        cli,
        ["--uri", tmp_uri, "enqueue", "--topic", "test-topic"],
        input="enqueue-from-stdin\n",
    )
    assert result.exit_code == 0, f"Error: {result.output}"
    assert "enqueue-from-stdin" in result.output

    # Verify the message was enqueued
    front_result = runner.invoke(cli, ["--uri", tmp_uri, "front", "--topic", "test-topic"])
    assert front_result.exit_code == 0
    assert "enqueue-from-stdin" in front_result.output


def test_push_no_payload(tmp_uri):
    """
    Ensure that `push` fails with exit code 1 if no payload is given
    (neither arg nor stdin).
    """
    runner = CliRunner()
    # No argument, no stdin:
    result = runner.invoke(cli, ["--uri", tmp_uri, "push"], input="")
    assert result.exit_code == 1, f"Output:\n{result.output}"
    assert "No payload provided" in result.output


def test_enqueue_no_payload(tmp_uri):
    """
    Ensure that `enqueue` fails with exit code 1 if no payload is given
    (neither arg nor stdin).
    """
    runner = CliRunner()
    # No argument, no stdin:
    result = runner.invoke(
        cli,
        ["--uri", tmp_uri, "enqueue", "--topic", "test-topic"],
        input="",  # empty stdin
    )
    assert result.exit_code == 1, f"Output:\n{result.output}"
    assert "No payload provided" in result.output


def test_search_dead(tmp_uri):
    """
    Test 'lzqueue search' with and without --dead.
    """
    runner = CliRunner()

    # add: dead-item
    runner.invoke(
        cli,
        [
            "--uri",
            tmp_uri,
            "enqueue",
            "dead-item",
            "--max-claims",
            "1",
            "--timeout",
            "0",
        ],
    )

    # Add: alive-item
    runner.invoke(cli, ["--uri", tmp_uri, "enqueue", "alive-item"])

    # Claim the "dead-item"
    runner.invoke(cli, ["--uri", tmp_uri, "dequeue"])

    # search => should only show "alive-item"
    result = runner.invoke(cli, ["--uri", tmp_uri, "search"])
    assert result.exit_code == 0
    lines = result.output.strip().split("\n")
    assert len(lines) == 1  # just one line
    alive_data = json.loads(lines[0])
    assert alive_data["payload"] == "alive-item"

    # Claim the "dead-item"
    runner.invoke(cli, ["--uri", tmp_uri, "dequeue"])

    # search --dead => should only show "dead-item"
    result_dead = runner.invoke(cli, ["--uri", tmp_uri, "search", "--dead"])
    assert result_dead.exit_code == 0
    lines_dead = result_dead.output.strip().split("\n")
    assert len(lines_dead) == 1
    dead_data = json.loads(lines_dead[0])
    assert dead_data["payload"] == "dead-item"
