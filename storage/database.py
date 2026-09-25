import sqlite3
import json
from pathlib import Path

from core.events import LEAFEvent


class LEAFDatabase:

    def __init__(self, database_path: str = "data/leaf.db"):

        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self._initialize()

    def _initialize(self):

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT
            )
            """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                source TEXT NOT NULL,
                session_id TEXT,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

    # -------------------------
    # Session operations
    # -------------------------

    def save_session(self, session):

        self.connection.execute(
            """
            INSERT INTO sessions (
                session_id,
                started_at,
                ended_at
            )
            VALUES (?, ?, ?)
            """,
            (
                session.session_id,
                session.started_at,
                session.ended_at,
            ),
        )

        self.connection.commit()

    def update_session(self, session):

        self.connection.execute(
            """
            UPDATE sessions
            SET ended_at = ?
            WHERE session_id = ?
            """,
            (
                session.ended_at,
                session.session_id,
            ),
        )

        self.connection.commit()

    def count_sessions(self):

        cursor = self.connection.execute(
            "SELECT COUNT(*) FROM sessions"
        )

        return cursor.fetchone()[0]

    def get_sessions(self):

        cursor = self.connection.execute(
            """
            SELECT
                session_id,
                started_at,
                ended_at
            FROM sessions
            ORDER BY id ASC
            """
        )

        rows = cursor.fetchall()

        sessions = []

        for row in rows:

            session_id = row[0]
            started_at = row[1]
            ended_at = row[2]

            event_cursor = self.connection.execute(
                """
                SELECT COUNT(*)
                FROM events
                WHERE session_id = ?
                """,
                (session_id,),
            )

            event_count = event_cursor.fetchone()[0]

            sessions.append({
                "session_id": session_id,
                "started_at": started_at,
                "ended_at": ended_at,
                "status": (
                    "completed"
                    if ended_at
                    else "running"
                ),
                "event_count": event_count,
            })

        return sessions

    def get_session(self, session_id):

        cursor = self.connection.execute(
            """
            SELECT
                session_id,
                started_at,
                ended_at
            FROM sessions
            WHERE session_id = ?
            """,
            (session_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        event_cursor = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM events
            WHERE session_id = ?
            """,
            (session_id,),
        )

        event_count = event_cursor.fetchone()[0]

        return {
            "session_id": row[0],
            "started_at": row[1],
            "ended_at": row[2],
            "status": (
                "completed"
                if row[2]
                else "running"
            ),
            "event_count": event_count,
        }

    # -------------------------
    # Event operations
    # -------------------------

    def save_event(self, event: LEAFEvent):

        self.connection.execute(
            """
            INSERT INTO events (
                event_type,
                source,
                session_id,
                timestamp,
                data
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.event_type,
                event.source,
                event.session_id,
                event.timestamp,
                json.dumps(event.data),
            ),
        )

        self.connection.commit()

    def count_events(self):

        cursor = self.connection.execute(
            "SELECT COUNT(*) FROM events"
        )

        return cursor.fetchone()[0]

    # -------------------------
    # Event queries
    # -------------------------

    def get_events(self):

        cursor = self.connection.execute(
            """
            SELECT
                id,
                event_type,
                source,
                session_id,
                timestamp,
                data
            FROM events
            ORDER BY id ASC
            """
        )

        rows = cursor.fetchall()

        events = []

        for row in rows:

            events.append({
                "id": row[0],
                "event_type": row[1],
                "source": row[2],
                "session_id": row[3],
                "timestamp": row[4],
                "data": json.loads(row[5]),
            })

        return events

    def get_events_by_session(self, session_id):

        cursor = self.connection.execute(
            """
            SELECT
                id,
                event_type,
                source,
                session_id,
                timestamp,
                data
            FROM events
            WHERE session_id = ?
            ORDER BY id ASC
            """,
            (session_id,),
        )

        rows = cursor.fetchall()

        events = []

        for row in rows:

            events.append({
                "id": row[0],
                "event_type": row[1],
                "source": row[2],
                "session_id": row[3],
                "timestamp": row[4],
                "data": json.loads(row[5]),
            })

        return events

    def get_events_by_type(self, event_type):

        cursor = self.connection.execute(
            """
            SELECT
                id,
                event_type,
                source,
                session_id,
                timestamp,
                data
            FROM events
            WHERE event_type = ?
            ORDER BY id ASC
            """,
            (event_type,),
        )

        rows = cursor.fetchall()

        events = []

        for row in rows:

            events.append({
                "id": row[0],
                "event_type": row[1],
                "source": row[2],
                "session_id": row[3],
                "timestamp": row[4],
                "data": json.loads(row[5]),
            })

        return events

    # -------------------------
    # Database lifecycle
    # -------------------------

    def close(self):
        self.connection.close()
