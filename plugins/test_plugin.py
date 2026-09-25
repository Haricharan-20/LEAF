from plugins.base import LEAFPlugin
from experiments.base import LEAFExperiment


class PluginInfoExperiment(LEAFExperiment):

    name = "plugin_info"

    description = (
        "Safe experiment registered by the LEAF test plugin."
    )

    version = "1.0"

    category = "plugin"

    risk_level = "low"

    required_capabilities = [
        "storage.read"
    ]

    def run(self, context):

        context.require_capability(
            "storage.read"
        )

        events = context.require_service(
            "events"
        )

        return events.emit(
            event_type="experiment.plugin_info",
            source="plugin.test",
            data={
                "plugin": "test",
                "message": (
                    "This experiment was registered "
                    "by the LEAF test plugin."
                ),
            },
        )


class TestPlugin(LEAFPlugin):

    name = "test"

    version = "1.0"

    description = (
        "Safe local plugin used to verify "
        "the LEAF plugin architecture."
    )

    def register(self, registry):

        registry.register(self)

        registry.register_experiment(
            PluginInfoExperiment
        )
