CREATE_TABLE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
CREATE TABLE IF NOT EXISTS messages (
    message_id   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    unique_id    TEXT,
    priority     INTEGER NOT NULL DEFAULT 0,
    topic        TEXT,
    payload      TEXT NOT NULL,
    timeout      REAL NOT NULL DEFAULT 600.0,
    claims       INTEGER NOT NULL DEFAULT 0,
    max_claims   INTEGER NOT NULL DEFAULT 2,
    delay        REAL NOT NULL DEFAULT 0.0,
    queued_for   TEXT,
    received_by  TEXT,
    added_at     REAL NOT NULL DEFAULT (unixepoch('subsec')),
    claimed_at   REAL NOT NULL DEFAULT 0.0,
    completed_at REAL NOT NULL DEFAULT 0.0
);
"""

CREATE_INDEXES = [
    """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
CREATE INDEX IF NOT EXISTS idx_messages_added_at
    ON messages (added_at);
""",
    """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_unique_id
    ON messages(unique_id)
    WHERE unique_id IS NOT NULL;
""",
]

INSERT_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
INSERT INTO messages (
    payload,
    topic,
    queued_for,
    priority,
    unique_id,
    delay,
    timeout,
    max_claims,
    added_at
)
VALUES (
    :payload,
    COALESCE(:topic, NULL),
    COALESCE(:for, NULL),
    COALESCE(:priority, 0),
    COALESCE(:unique_id, NULL),
    COALESCE(:delay, 0),
    COALESCE(:timeout, 600),
    COALESCE(:max_claims, 2),
    unixepoch('subsec')
)
RETURNING
    message_id,
    payload,
    topic,
    queued_for,
    priority,
    unique_id,
    delay,
    timeout,
    max_claims,
    added_at,
    claimed_at,
    completed_at,
    claims;
"""

DEQUEUE_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
WITH next_msg AS (
    SELECT message_id
      FROM messages
     WHERE completed_at = 0
       AND ( :topic IS NULL OR topic = :topic )
       AND ( :for   IS NULL OR queued_for = :for )
       AND ( :after IS NULL OR added_at >= :after )
       AND ( :before IS NULL OR added_at <= :before )
       AND (added_at + delay) <= unixepoch('subsec')
       AND claims < max_claims
       AND (
              claimed_at = 0
              OR (claimed_at + timeout <= unixepoch('subsec'))
           )
  ORDER BY priority DESC, added_at ASC, message_id ASC
     LIMIT 1
)
UPDATE messages
   SET claimed_at = unixepoch('subsec'),
       claims     = claims + 1,
       received_by = COALESCE(:by, received_by),
       completed_at = CASE WHEN :no_ack = 1 THEN unixepoch('subsec') ELSE completed_at END
 WHERE message_id = (SELECT message_id FROM next_msg)
RETURNING
    message_id,
    payload,
    topic,
    queued_for,
    received_by,
    priority,
    unique_id,
    delay,
    timeout,
    max_claims,
    claims,
    added_at,
    claimed_at,
    completed_at;
"""

ACK_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
UPDATE messages
   SET completed_at = unixepoch('subsec')
 WHERE message_id = :message_id
   AND completed_at = 0
RETURNING
    message_id,
    payload,
    topic,
    queued_for,
    received_by,
    priority,
    unique_id,
    delay,
    timeout,
    max_claims,
    claims,
    added_at,
    claimed_at,
    completed_at;
"""

POP_MESSAGE_LIFO = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
WITH next_msg AS (
    SELECT message_id
      FROM messages
     WHERE completed_at = 0
       AND claimed_at = 0
       AND (added_at + delay) <= unixepoch('subsec')
       AND claims < max_claims
  ORDER BY added_at DESC, message_id DESC
     LIMIT 1
)
UPDATE messages
   SET claimed_at   = unixepoch('subsec'),
       claims       = claims + 1,
       received_by  = COALESCE(:by, received_by),
       completed_at = unixepoch('subsec')
 WHERE message_id = (SELECT message_id FROM next_msg)
RETURNING
    message_id,
    payload,
    topic,
    queued_for,
    received_by,
    priority,
    unique_id,
    delay,
    timeout,
    max_claims,
    claims,
    added_at,
    claimed_at,
    completed_at;
"""

FRONT_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
SELECT *
  FROM messages
 WHERE completed_at = 0
   AND ( :topic  IS NULL OR topic = :topic )
   AND ( :for    IS NULL OR queued_for = :for )
   AND ( :by     IS NULL OR received_by = :by )
   AND ( :after  IS NULL OR added_at >= :after )
   AND ( :before IS NULL OR added_at <= :before )
   AND (added_at + delay) <= unixepoch('subsec')
   AND claims < max_claims
   AND (
         claimed_at = 0
         OR (claimed_at + timeout <= unixepoch('subsec'))
       )
 ORDER BY message_id ASC
 LIMIT 1;
"""

BACK_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
SELECT *
  FROM messages
 WHERE completed_at = 0
   AND ( :topic  IS NULL OR topic = :topic )
   AND ( :for    IS NULL OR queued_for = :for )
   AND ( :by     IS NULL OR received_by = :by )
   AND ( :after  IS NULL OR added_at >= :after )
   AND ( :before IS NULL OR added_at <= :before )
   AND (added_at + delay) <= unixepoch('subsec')
   AND claims < max_claims
   AND (
         claimed_at = 0
         OR (claimed_at + timeout <= unixepoch('subsec'))
       )
 ORDER BY message_id DESC
 LIMIT 1;
"""

CLAIMED_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
SELECT *
  FROM messages
 WHERE completed_at = 0
   AND ( :topic  IS NULL OR topic = :topic )
   AND ( :for    IS NULL OR queued_for = :for )
   AND ( :by     IS NULL OR received_by = :by )
   AND ( :after  IS NULL OR claimed_at >= :after )
   AND ( :before IS NULL OR claimed_at <= :before )
   AND claimed_at > 0
   AND (claimed_at + timeout >= unixepoch('subsec'))
 ORDER BY claimed_at DESC
 LIMIT 1;
"""

COMPLETED_MESSAGE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
SELECT *
  FROM messages
 WHERE completed_at > 0
   AND ( :topic  IS NULL OR topic = :topic )
   AND ( :for    IS NULL OR queued_for = :for )
   AND ( :by     IS NULL OR received_by = :by )
   AND ( :after  IS NULL OR completed_at >= :after )
   AND ( :before IS NULL OR completed_at <= :before )
 ORDER BY completed_at DESC
 LIMIT 1;
"""

STATUS_QUERY = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
SELECT
  (SELECT COUNT(*) FROM messages) AS total,
  (SELECT COUNT(*) FROM messages WHERE claimed_at = 0 AND completed_at = 0) AS unclaimed,
  (SELECT COUNT(*) FROM messages WHERE completed_at > 0) AS completed
"""

DELETE_BEFORE = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
DELETE FROM messages
 WHERE added_at <= :before
"""

SEARCH_MESSAGES = """
-- noinspection SqlConstantExpression, SqlResolve, SqlSignature
SELECT *
  FROM messages
 WHERE 1 = 1
   AND ( :topic  IS NULL OR topic = :topic )
   AND ( :for    IS NULL OR queued_for = :for )
   AND ( :by     IS NULL OR received_by = :by )
   AND ( :after  IS NULL OR added_at >= :after )
   AND ( :before IS NULL OR added_at <= :before )
   AND (
         :completed = 0
         OR completed_at > 0
       )
   AND (
         :claimed = 0
         OR (
            completed_at = 0
            AND claimed_at > 0
            AND (claimed_at + timeout) > unixepoch('subsec')
         )
       )
   AND (
         :dead = 0
         OR (
            completed_at = 0
            AND claimed_at > 0
            AND (claimed_at + timeout) <= unixepoch('subsec')
            AND claims >= max_claims
         )
       )

   AND (
         :queued = 0
         OR (
            completed_at=0
            AND (
              claimed_at=0
              OR (claimed_at+timeout <= unixepoch('subsec'))
            )
            AND claims<max_claims
         )
    )
 ORDER BY added_at ASC
 LIMIT :limit;
"""
