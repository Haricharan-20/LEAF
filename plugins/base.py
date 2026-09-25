from abc import ABC, abstractmethod


class LEAFPlugin(ABC):

    name = "unnamed"
    version = "1.0"
    description = "No description provided."

    @abstractmethod
    def register(self, registry):
        pass

    @classmethod
    def metadata(cls):
        return {
            "name": cls.name,
            "version": cls.version,
            "description": cls.description,
        }
