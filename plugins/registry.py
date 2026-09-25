class LEAFPluginRegistry:

    def __init__(self):
        self.plugins = {}
        self.experiments = {}

    def register(self, plugin):
        self.plugins[plugin.name] = plugin

    def register_experiment(self, experiment):
        self.experiments[experiment.name] = experiment

    def get(self, name):
        return self.plugins.get(name)

    def get_experiment(self, name):
        return self.experiments.get(name)

    def list_plugins(self):
        return list(self.plugins.values())

    def list_experiments(self):
        return list(self.experiments.values())
