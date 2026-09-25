from core.capabilities import LEAFCapabilityManager
from core.engine import LEAFEngine
from core.session import LEAFSession
from core.services import LEAFEventService


class LEAFExecutionContext:

    def __init__(
        self,
        engine: LEAFEngine,
        session: LEAFSession,
        capability_manager: LEAFCapabilityManager,
    ):

        self.engine = engine
        self.session = session
        self.capabilities = capability_manager

        self.events = LEAFEventService(
            engine
        )

    def has_capability(self, capability):

        return self.capabilities.is_allowed(
            capability
        )

    def require_capability(self, capability):

        if not self.has_capability(
            capability
        ):

            raise PermissionError(
                "Capability not authorized: "
                + capability
            )
