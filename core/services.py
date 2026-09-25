from core.engine import LEAFEngine
from core.service_base import LEAFService


class LEAFEventService(LEAFService):

    name = "events"

    required_capability = "storage.read"

    def __init__(
        self,
        engine: LEAFEngine,
        capability_manager,
    ):

        super().__init__(
            capability_manager
        )

        self.engine = engine

    def emit(
        self,
        event_type,
        source,
        data=None,
    ):

        self.check_capability()

        return self.engine.emit(
            event_type=event_type,
            source=source,
            data=data,
        )
