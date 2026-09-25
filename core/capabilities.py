from dataclasses import dataclass


@dataclass(frozen=True)
class LEAFCapability:

    name: str
    description: str


CAPABILITIES = {

    "system.read": LEAFCapability(
        name="system.read",
        description=(
            "Read basic information about "
            "the LEAF execution environment."
        ),
    ),

    "network.read": LEAFCapability(
        name="network.read",
        description=(
            "Perform approved read-only "
            "network operations."
        ),
    ),

    "browser.read": LEAFCapability(
        name="browser.read",
        description=(
            "Read information from an approved "
            "controlled browser environment."
        ),
    ),

    "storage.read": LEAFCapability(
        name="storage.read",
        description=(
            "Read LEAF-managed research data."
        ),
    ),
}


class LEAFCapabilityManager:

    def __init__(
        self,
        allowed_capabilities=None,
    ):

        if allowed_capabilities is None:

            allowed_capabilities = set(
                CAPABILITIES.keys()
            )

        self.capabilities = dict(
            CAPABILITIES
        )

        self.allowed_capabilities = set(
            allowed_capabilities
        )

    def get(self, name):

        return self.capabilities.get(name)

    def exists(self, name):

        return name in self.capabilities

    def is_allowed(self, name):

        return (
            name in self.capabilities
            and name in self.allowed_capabilities
        )

    def list(self):

        return list(
            self.capabilities.values()
        )

    def list_allowed(self):

        return [
            capability
            for capability in self.capabilities.values()
            if self.is_allowed(
                capability.name
            )
        ]

    def validate(
        self,
        required_capabilities,
    ):

        missing = []

        for capability in (
            required_capabilities
        ):

            if not self.exists(
                capability
            ):

                missing.append(
                    capability
                )

        return missing

    def authorize(
        self,
        required_capabilities,
    ):

        denied = []

        for capability in (
            required_capabilities
        ):

            if not self.is_allowed(
                capability
            ):

                denied.append(
                    capability
                )

        return denied
