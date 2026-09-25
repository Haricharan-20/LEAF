class LEAFServiceRegistry:

    def __init__(self):

        self.services = {}

    def register(self, service):

        self.services[
            service.name
        ] = service

    def get(self, name):

        return self.services.get(name)

    def list(self):

        return list(
            self.services.values()
        )

    def names(self):

        return list(
            self.services.keys()
        )

    def metadata(self):

        return [
            service.metadata()
            for service in self.services.values()
        ]

    def metadata_for(self, name):

        service = self.get(name)

        if service is None:

            return None

        return service.metadata()
