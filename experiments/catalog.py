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

    def create(self, name):

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

        return experiment_class()
