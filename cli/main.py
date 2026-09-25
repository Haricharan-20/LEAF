from core.runner import LEAFExperimentRunner
from core.capabilities import LEAFCapabilityManager
from storage.database import LEAFDatabase

from experiments.catalog import LEAFExperimentCatalog


# --------------------------------------------------
# Experiment catalog
# --------------------------------------------------

def get_catalog():

    return LEAFExperimentCatalog()


# --------------------------------------------------
# Help
# --------------------------------------------------

def show_help():

    print()
    print("LEAF commands:")
    print()

    print("  experiments")
    print("      List available experiments.")
    print()

    print("  experiment <name>")
    print("      Show experiment metadata.")
    print()

    print("  capabilities")
    print("      Show available and allowed capabilities.")
    print()

    print("  run <name>")
    print("      Run an experiment.")
    print()

    print("  sessions")
    print("      List research sessions.")
    print()

    print("  session <session_id>")
    print("      Show a research session.")
    print()

    print("  events")
    print("      List stored events.")
    print()

    print("  events type <event_type>")
    print("      List events by type.")
    print()

    print("  events session <session_id>")
    print("      List events from a session.")
    print()

    print("  help")
    print("      Show this help message.")
    print()

    print("  services")
    print("      List available LEAF services.")
    print()

    print("  exit")
    print("      Exit LEAF.")
    print()


# --------------------------------------------------
# Capability display
# --------------------------------------------------

def show_capabilities():

    manager = LEAFCapabilityManager()

    print()
    print("LEAF capabilities:")
    print()

    print("Available capabilities:")
    print()

    for capability in manager.list():

        status = (
            "ALLOWED"
            if manager.is_allowed(
                capability.name
            )
            else "DENIED"
        )

        print(
            f"  {capability.name}"
        )

        print(
            f"      {capability.description}"
        )

        print(
            f"      Status: {status}"
        )

        print()

    print(
        "Allowed capabilities:"
    )

    print()

    allowed = manager.list_allowed()

    if not allowed:

        print("  None")

    else:

        for capability in allowed:

            print(
                f"  {capability.name}"
            )

    print()


# --------------------------------------------------
# Experiment listing
# --------------------------------------------------

def list_experiments():

    catalog = get_catalog()

    print()
    print("Available experiments:")
    print()

    for experiment_class in catalog.list():

        print(
            f"  {experiment_class.name}"
        )

        print(
            f"      {experiment_class.description}"
        )

    print()


# --------------------------------------------------
# Experiment details
# --------------------------------------------------

def show_experiment(name):

    catalog = get_catalog()

    experiment_class = catalog.get(name)

    print()

    if experiment_class is None:

        print(
            f"Experiment not found: {name}"
        )

        print()

        return

    metadata = experiment_class.metadata()

    print("Experiment:")
    print()

    print(
        f"Name:                 "
        f"{metadata['name']}"
    )

    print(
        f"Description:          "
        f"{metadata['description']}"
    )

    print(
        f"Version:              "
        f"{metadata['version']}"
    )

    print(
        f"Category:             "
        f"{metadata['category']}"
    )

    print(
        f"Risk level:           "
        f"{metadata['risk_level']}"
    )

    print(
        "Required capabilities:",
        ", ".join(
            metadata["required_capabilities"]
        )
        if metadata["required_capabilities"]
        else "none",
    )

    print()


# --------------------------------------------------
# Event display
# --------------------------------------------------

def print_events(events):

    if not events:

        print()
        print("No events found.")
        print()

        return

    print()

    for event in events:

        print(
            f"ID:        {event['id']}"
        )

        print(
            f"Type:      {event['event_type']}"
        )

        print(
            f"Source:    {event['source']}"
        )

        print(
            f"Session:   {event['session_id']}"
        )

        print(
            f"Timestamp: {event['timestamp']}"
        )

        print(
            f"Data:      {event['data']}"
        )

        print("-" * 50)

    print()


# --------------------------------------------------
# Event queries
# --------------------------------------------------

def list_events():

    database = LEAFDatabase()

    try:

        events = database.get_events()

        print_events(events)

    finally:

        database.close()


def list_events_by_type(event_type):

    database = LEAFDatabase()

    try:

        events = (
            database.get_events_by_type(
                event_type
            )
        )

        print_events(events)

    finally:

        database.close()


def list_events_by_session(session_id):

    database = LEAFDatabase()

    try:

        events = (
            database.get_events_by_session(
                session_id
            )
        )

        print_events(events)

    finally:

        database.close()


# --------------------------------------------------
# Session listing
# --------------------------------------------------

def list_sessions():

    database = LEAFDatabase()

    try:

        sessions = database.get_sessions()

        print()

        if not sessions:

            print("No sessions found.")
            print()

            return

        print("Research sessions:")
        print()

        for session in sessions:

            print(
                f"Session:  "
                f"{session['session_id']}"
            )

            print(
                f"Started:  "
                f"{session['started_at']}"
            )

            print(
                f"Ended:    "
                f"{session['ended_at']}"
            )

            print(
                f"Status:   "
                f"{session['status']}"
            )

            print(
                f"Events:   "
                f"{session['event_count']}"
            )

            print("-" * 60)

        print()

    finally:

        database.close()


# --------------------------------------------------
# Session details
# --------------------------------------------------

def show_session(session_id):

    database = LEAFDatabase()

    try:

        session = (
            database.get_session(
                session_id
            )
        )

        print()

        if session is None:

            print(
                f"Session not found: "
                f"{session_id}"
            )

            print()

            return

        print("Research session:")
        print()

        print(
            f"Session ID: "
            f"{session['session_id']}"
        )

        print(
            f"Started:    "
            f"{session['started_at']}"
        )

        print(
            f"Ended:      "
            f"{session['ended_at']}"
        )

        print(
            f"Status:     "
            f"{session['status']}"
        )

        print(
            f"Events:     "
            f"{session['event_count']}"
        )

        print()

        print("Session events:")

        events = (
            database.get_events_by_session(
                session_id
            )
        )

        print_events(events)

    finally:

        database.close()


# --------------------------------------------------
# Run experiment
# --------------------------------------------------

def run_experiment(name):

    catalog = get_catalog()

    experiment_class = catalog.get(name)

    if experiment_class is None:

        print()

        print(
            f"Error: Unknown experiment: "
            f"{name}"
        )

        print()

        return

    runner = LEAFExperimentRunner()

    print()

    print(
        f"Session: "
        f"{runner.session.session_id}"
    )

    print(
        f"Running experiment: "
        f"{name}"
    )

    print(
        f"Description: "
        f"{experiment_class.description}"
    )

    try:

        result = runner.run(name)

        print()

        print(
            "Experiment completed."
        )

        print(
            f"Event generated: "
            f"{result.event_type}"
        )

        print(
            "Event stored successfully."
        )

    except Exception as error:

        print()

        print(
            f"Experiment failed: "
            f"{error}"
        )

    finally:

        runner.close()

    print(
        f"Session ended: "
        f"{runner.session.ended_at}"
    )

    print()


# --------------------------------------------------
# Service display
# --------------------------------------------------
def show_services():

    runner = LEAFExperimentRunner()

    try:

        services = runner.context.service_metadata()

        print()
        print("LEAF services:")
        print()

        if not services:
            print("No services registered.")
            print()
            return

        print("Available services:")
        print()

        for service in services:

            print(
                f"  {service['name']}"
            )

            print(
                f"      {service['description']}"
            )

            print(
                f"      Version: {service['version']}"
            )

            capability = (
                service["required_capability"]
                or "none"
            )

            print(
                f"      Required capability: {capability}"
            )

            print()

    finally:

        runner.close()


# --------------------------------------------------
# CLI
# --------------------------------------------------

def start_cli():

    print(
        "Type 'help' for available commands."
    )

    print()

    while True:

        try:

            command = input(
                "LEAF> "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print()

            print(
                "Exiting LEAF."
            )

            break

        if not command:

            continue

        parts = command.split()

        action = parts[0].lower()

        # ------------------------------
        # Help
        # ------------------------------

        if action == "services":

            if len(parts) != 1:
                print(
                    "Usage: services"
                )
                continue

            show_services()
            continue

        if action == "help":

            show_help()

        # ------------------------------
        # Experiments
        # ------------------------------

        elif action == "experiments":

            if len(parts) != 1:

                print()

                print(
                    "Usage: experiments"
                )

                print()

                continue

            list_experiments()

        # ------------------------------
        # Experiment metadata
        # ------------------------------

        elif action == "experiment":

            if len(parts) != 2:

                print()

                print(
                    "Usage: "
                    "experiment <name>"
                )

                print()

                continue

            show_experiment(
                parts[1]
            )

        # ------------------------------
        # Capabilities
        # ------------------------------

        elif action == "capabilities":

            if len(parts) != 1:

                print()

                print(
                    "Usage: capabilities"
                )

                print()

                continue

            show_capabilities()

        # ------------------------------
        # Run experiment
        # ------------------------------

        elif action == "run":

            if len(parts) != 2:

                print()

                print(
                    "Usage: "
                    "run <experiment>"
                )

                print()

                continue

            run_experiment(
                parts[1]
            )

        # ------------------------------
        # Sessions
        # ------------------------------

        elif action == "sessions":

            if len(parts) != 1:

                print()

                print(
                    "Usage: sessions"
                )

                print()

                continue

            list_sessions()

        # ------------------------------
        # Session
        # ------------------------------

        elif action == "session":

            if len(parts) != 2:

                print()

                print(
                    "Usage: "
                    "session <session_id>"
                )

                print()

                continue

            show_session(
                parts[1]
            )

        # ------------------------------
        # Events
        # ------------------------------

        elif action == "events":

            if len(parts) == 1:

                list_events()

            elif len(parts) == 3:

                if (
                    parts[1].lower()
                    == "type"
                ):

                    list_events_by_type(
                        parts[2]
                    )

                elif (
                    parts[1].lower()
                    == "session"
                ):

                    list_events_by_session(
                        parts[2]
                    )

                else:

                    print()

                    print(
                        "Usage:"
                    )

                    print(
                        "  events"
                    )

                    print(
                        "  events type "
                        "<event_type>"
                    )

                    print(
                        "  events session "
                        "<session_id>"
                    )

                    print()

            else:

                print()

                print(
                    "Usage:"
                )

                print(
                    "  events"
                )

                print(
                    "  events type "
                    "<event_type>"
                )

                print(
                    "  events session "
                    "<session_id>"
                )

                print()

        # ------------------------------
        # Exit
        # ------------------------------

        elif action == "exit":

            print(
                "Exiting LEAF."
            )

            break

        # ------------------------------
        # Unknown command
        # ------------------------------

        else:

            print()

            print(
                f"Unknown command: "
                f"{action}"
            )

            print(
                "Type 'help' "
                "to see available commands."
            )

            print()


if __name__ == "__main__":

    start_cli()
