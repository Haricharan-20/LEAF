from abc import ABC, abstractmethod


class LEAFExperiment(ABC):

    name = "unnamed"

    description = "No description provided."

    version = "1.0"

    category = "general"

    risk_level = "low"

    required_capabilities = []

    @abstractmethod
    def run(self, context):
        pass

    @classmethod
    def metadata(cls):

        return {
            "name": cls.name,
            "description": cls.description,
            "version": cls.version,
            "category": cls.category,
            "risk_level": cls.risk_level,
            "required_capabilities": cls.required_capabilities,
        }
