from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class LEAFEvent:

    event_type: str
    source: str
    data: dict[str, Any] = field(default_factory=dict)
    session_id: str | None = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source": self.source,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "data": self.data,
        }
