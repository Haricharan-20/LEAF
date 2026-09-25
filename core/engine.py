from core.events import LEAFEvent


class LEAFEngine:

    def __init__(self, session_id: str | None = None):
        self.session_id = session_id
        self.events: list[LEAFEvent] = []

    def emit(
        self,
        event_type: str,
        source: str,
        data: dict | None = None,
    ) -> LEAFEvent:

        event = LEAFEvent(
            event_type=event_type,
            source=source,
            session_id=self.session_id,
            data=data or {},
        )

        self.events.append(event)

        return event

    def get_events(self) -> list[LEAFEvent]:
        return self.events
