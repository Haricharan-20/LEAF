from core.capabilities import LEAFCapabilityManager


class LEAFService:

    name = "unnamed"

    required_capability = None

    def __init__(
        self,
        capability_manager: LEAFCapabilityManager,
    ):

        self.capabilities = capability_manager

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
