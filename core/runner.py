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

    def run(self, experiment_name):

        experiment = self.catalog.create(
            experiment_name
        )

        result = experiment.run(
            self.engine
        )

        self.database.save_event(
            result
        )

        return result

    def close(self):

        self.session.finish()

        self.database.update_session(
            self.session
        )

        self.database.close()
