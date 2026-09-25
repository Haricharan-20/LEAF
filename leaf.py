#!/usr/bin/env python3

from datetime import datetime

from core.engine import LEAFEngine
from storage.database import LEAFDatabase
from experiments.registry import get_experiment


BANNER = r"""
╔══════════════════════════════════════════════╗
║                    LEAF                      ║
║   Layered Exploration & Analysis Framework   ║
║                                              ║
║             Research Edition v0.4            ║
╚══════════════════════════════════════════════╝
"""


def main():

    print(BANNER)

    print(
        f"Started: "
        f"{datetime.now().isoformat(timespec='seconds')}"
    )

    engine = LEAFEngine()
    database = LEAFDatabase()

    # Record system startup
    startup_event = engine.emit(
        event_type="system.start",
        source="leaf.core",
        data={
            "version": "0.4.0",
            "environment": "termux",
        },
    )

    database.save_event(startup_event)

    # Load experiment
    experiment = get_experiment("system_info")

    print()
    print(f"Experiment: {experiment.name}")
    print(f"Description: {experiment.description}")

    # Run experiment
    result = experiment.run(engine)

    # Store result
    database.save_event(result)

    print()
    print("Experiment completed.")
    print(f"Event generated: {result.event_type}")
    print(f"Events in current session: {len(engine.get_events())}")
    print(f"Events stored in database: {database.count_events()}")

    database.close()


if __name__ == "__main__":
    main()
