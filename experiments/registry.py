from experiments.system_info import SystemInfoExperiment


EXPERIMENTS = {
    SystemInfoExperiment.name: SystemInfoExperiment,
}


def get_experiment(name):
    experiment_class = EXPERIMENTS.get(name)

    if experiment_class is None:
        raise ValueError(
            f"Unknown experiment: {name}"
        )

    return experiment_class()
