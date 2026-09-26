from core.context import LEAFExecutionContext
from core.engine import LEAFEngine
from core.session import LEAFSession
from storage.database import LEAFDatabase

from experiments.catalog import LEAFExperimentCatalog


class LEAFExperimentRunner:

    def __init__(
        self,
        allowed_capabilities=None,
    ):

        self.database = LEAFDatabase()

        self.session = LEAFSession.create()

        self.database.save_session(
            self.session
        )

        self.engine = LEAFEngine(
            session_id=self.session.session_id
        )

        self.catalog = LEAFExperimentCatalog(
            allowed_capabilities=(
                allowed_capabilities
            )
        )

        self.context = LEAFExecutionContext(
            engine=self.engine,
            session=self.session,
            capability_manager=(
                self.catalog.capability_manager
            ),
        )

        self.context.initialize_services()
        self.context.start_services()

    def run(self, experiment_name):

        experiment = self.catalog.create(
            experiment_name,
            service_registry=self.context.services,
        )

        result = experiment.run(
            self.context
        )

        self.database.save_event(
            result
        )

        return result

    def close(self):

        self.context.stop_services()

        self.session.finish()

        self.database.update_session(
            self.session
        )

        self.database.close()
