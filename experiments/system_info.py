import platform

from experiments.base import LEAFExperiment


class SystemInfoExperiment(LEAFExperiment):

    name = "system_info"

    description = (
        "Collect basic information about the LEAF "
        "execution environment."
    )

    version = "1.0"

    category = "environment"

    risk_level = "low"

    required_capabilities = [
        "system.read"
    ]

    def run(self, context):

        context.require_capability(
            "system.read"
        )

        information = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python": platform.python_version(),
        }

        return context.events.emit(
            event_type="experiment.system_info",
            source="experiment.system_info",
            data=information,
        )
