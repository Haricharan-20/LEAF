from core.capabilities import LEAFCapabilityManager
from core.engine import LEAFEngine
from core.session import LEAFSession
from core.services import LEAFEventService
from core.service_registry import LEAFServiceRegistry


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

        self.services = LEAFServiceRegistry()

        events = LEAFEventService(
            engine=engine,
            capability_manager=capability_manager,
        )

        self.services.register(
            events
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

    def get_service(self, name):

        return self.services.get(name)

    def require_service(self, name):

        service = self.get_service(name)

        if service is None:

            raise ValueError(
                "Unknown service: "
                + name
            )

        return service

    def list_services(self):

        return self.services.names()

    def service_metadata(self):

        return self.services.metadata()

    def initialize_services(self):

        self.services.initialize_all()

    def start_services(self):

        self.services.start_all()

    def stop_services(self):

        self.services.stop_all()

    def service_states(self):

        return self.services.states()

    def service_status(self):

        return self.services.status()

    def ready_services(self):

        return [
            service.name
            for service in self.services.ready_services()
        ]

    def all_services_ready(self):

        return self.services.all_ready()

    def require_ready_service(self, name):

        return self.services.require_ready(
            name
        )
