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

    def validate_requirements(
        self,
        experiment_class,
        service_registry=None,
    ):

        report = {
            "valid": True,
            "unknown_capabilities": [],
            "unauthorized_capabilities": [],
            "unknown_services": [],
            "unready_services": [],
            "service_validation_missing": [],
        }

        required_capabilities = (
            experiment_class.required_capabilities
        )

        report[
            "unknown_capabilities"
        ] = (
            self.capability_manager.validate(
                required_capabilities
            )
        )

        report[
            "unauthorized_capabilities"
        ] = (
            self.capability_manager.authorize(
                required_capabilities
            )
        )

        required_services = (
            experiment_class.required_services
        )

        if (
            required_services
            and service_registry is None
        ):

            report[
                "service_validation_missing"
            ] = list(
                required_services
            )

        elif service_registry is not None:

            for service_name in required_services:

                service = service_registry.get(
                    service_name
                )

                if service is None:

                    report[
                        "unknown_services"
                    ].append(
                        service_name
                    )

                elif not service.is_ready():

                    report[
                        "unready_services"
                    ].append(
                        service_name
                    )

        report["valid"] = not any(
            (
                report[
                    "unknown_capabilities"
                ],
                report[
                    "unauthorized_capabilities"
                ],
                report[
                    "unknown_services"
                ],
                report[
                    "unready_services"
                ],
                report[
                    "service_validation_missing"
                ],
            )
        )

        return report

    def validate_services(
        self,
        service_registry,
        required_services,
    ):

        report = self.validate_requirements(
            type(
                "ServiceRequirement",
                (),
                {
                    "required_capabilities": [],
                    "required_services": (
                        required_services
                    ),
                },
            ),
            service_registry,
        )

        unavailable = []

        unavailable.extend(
            service
            + " (unknown)"
            for service in (
                report["unknown_services"]
            )
        )

        unavailable.extend(
            service
            + " (not ready)"
            for service in (
                report["unready_services"]
            )
        )

        return unavailable

    def requirements(
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

        return self.validate_requirements(
            experiment_class,
            service_registry,
        )

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

        report = self.validate_requirements(
            experiment_class,
            service_registry,
        )

        if report["unknown_capabilities"]:

            raise ValueError(
                "Experiment requires "
                "unknown capabilities: "
                + ", ".join(
                    report[
                        "unknown_capabilities"
                    ]
                )
            )

        if report["unauthorized_capabilities"]:

            raise PermissionError(
                "Experiment requires "
                "unauthorized capabilities: "
                + ", ".join(
                    report[
                        "unauthorized_capabilities"
                    ]
                )
            )

        if report["service_validation_missing"]:

            raise ValueError(
                "Experiment requires "
                "service validation: "
                + ", ".join(
                    report[
                        "service_validation_missing"
                    ]
                )
            )

        if report["unknown_services"]:

            raise ValueError(
                "Experiment requires "
                "unknown services: "
                + ", ".join(
                    report[
                        "unknown_services"
                    ]
                )
            )

        if report["unready_services"]:

            raise RuntimeError(
                "Experiment requires "
                "ready services: "
                + ", ".join(
                    report[
                        "unready_services"
                    ]
                )
            )

        return experiment_class()
