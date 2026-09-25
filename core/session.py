from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class LEAFSession:

    session_id: str
    started_at: str
    ended_at: str | None = None

    @classmethod
    def create(cls):
        return cls(
            session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc).isoformat(),
        )

    def finish(self):
        self.ended_at = datetime.now(timezone.utc).isoformat()
