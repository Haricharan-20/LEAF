from core.engine import LEAFEngine


class LEAFEventService:

    def __init__(self, engine: LEAFEngine):

        self.engine = engine

    def emit(
        self,
        event_type,
        source,
        data=None,
    ):

        return self.engine.emit(
            event_type=event_type,
            source=source,
            data=data,
        )
