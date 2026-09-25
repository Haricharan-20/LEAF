from core.capabilities import LEAFCapabilityManager


class LEAFService:

    name = "unnamed"

    description = "No description provided."

    version = "1.0"

    required_capability = None

    def __init__(
        self,
        capability_manager: LEAFCapabilityManager,
    ):

        self.capabilities = capability_manager
        self.state = "created"

    def initialize(self):

        if self.state != "created":
            return

        self.state = "initialized"

    def start(self):

        if self.state == "created":
            self.initialize()

        if self.state != "initialized":
            return

        self.state = "available"

    def stop(self):

        if self.state == "available":
            self.state = "closed"

    def is_ready(self):

        return self.state == "available"

    def require_ready(self):

        if not self.is_ready():

            raise RuntimeError(
                "Service is not ready: "
                + self.name
            )

    def status(self):

        return {
            "name": self.name,
            "state": self.state,
            "ready": self.is_ready(),
        }

    def check_capability(self):

        if (
            self.required_capability
            and not self.capabilities.is_allowed(
                self.required_capability
            )
        ):

            raise PermissionError(
                "Service requires capability: "
                + self.required_capability
            )

    @classmethod
    def metadata(cls):

        return {
            "name": cls.name,
            "description": cls.description,
            "version": cls.version,
            "required_capability": (
                cls.required_capability
            ),
        }
