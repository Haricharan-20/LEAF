from experiments.registry import EXPERIMENTS
from plugins.registry import LEAFPluginRegistry
from plugins.loader import discover_plugins

from core.capabilities import LEAFCapabilityManager


class LEAFExperimentCatalog:

    def __init__(
        self,
        allowed_capabilities=None,
    ):

        self.experiments = {}

        self.capability_manager = (
            LEAFCapabilityManager(
                allowed_capabilities
            )
        )

        self._load_builtin_experiments()
        self._load_plugin_experiments()

    def _load_builtin_experiments(self):

        for name, experiment_class in (
            EXPERIMENTS.items()
        ):

            self.experiments[
                name
            ] = experiment_class

    def _load_plugin_experiments(self):

        self.plugin_registry = (
            LEAFPluginRegistry()
        )

        discover_plugins(
            self.plugin_registry
        )

        for experiment_class in (
            self.plugin_registry.list_experiments()
        ):

            self.experiments[
                experiment_class.name
            ] = experiment_class

    def get(self, name):

        return self.experiments.get(name)

    def list(self):

        return list(
            self.experiments.values()
        )

    def names(self):

        return list(
            self.experiments.keys()
        )

    def validate_services(
        self,
        service_registry,
        required_services,
    ):

        unavailable = []

        for service_name in required_services:

            service = service_registry.get(
                service_name
            )

            if service is None:

                unavailable.append(
                    service_name
                    + " (unknown)"
                )

            elif not service.is_ready():

                unavailable.append(
                    service_name
                    + " (not ready)"
                )

        return unavailable

    def create(
        self,
        name,
        service_registry=None,
    ):

        experiment_class = self.get(name)

        if experiment_class is None:

            raise ValueError(
                f"Unknown experiment: "
                f"{name}"
            )

        required = (
            experiment_class.required_capabilities
        )

        unknown = (
            self.capability_manager.validate(
                required
            )
        )

        if unknown:

            raise ValueError(
                "Experiment requires "
                "unknown capabilities: "
                + ", ".join(unknown)
            )

        denied = (
            self.capability_manager.authorize(
                required
            )
        )

        if denied:

            raise PermissionError(
                "Experiment requires "
                "unauthorized capabilities: "
                + ", ".join(denied)
            )

        required_services = (
            experiment_class.required_services
        )

        if (
            required_services
            and service_registry is None
        ):

            raise ValueError(
                "Experiment requires "
                "service validation: "
                + ", ".join(required_services)
            )

        if service_registry is not None:

            unknown_services = (
                self.validate_services(
                    service_registry,
                    required_services,
                )
            )

            if unknown_services:

                raise ValueError(
                    "Experiment requires "
                    "unknown services: "
                    + ", ".join(
                        unknown_services
                    )
                )

        return experiment_class()
