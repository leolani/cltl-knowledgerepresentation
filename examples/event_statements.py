"""
THIS SCRIPT FILLS IN THE BRAIN WITH BASIC INFORMATION REGARDING EACH OF THE TEAM'S DEVELOPERS,
FOR EXAMPLE, WHERE THEY ARE FROM, WHAT THEY LIKE, AND WHERE THEY LIVE.
FOR MORE INFORMATION ON WHAT INFORMATION PLEASE REFER TO cltl.brain.utils.base_cases
"""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from tqdm import tqdm

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.base_cases import events
from cltl.brain.utils.helper_functions import brain_response_to_json


def main(log_path):
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)
    for (context_capsule, statements_capsules) in tqdm(events):
        print(f"\n\n---------------------------------------------------------------\n")
        # Create context
        response = brain.capsule_context(context_capsule)

        for capsule in statements_capsules:
            # Add information to the brain
            response = brain.capsule_event(capsule, reason_types=True, return_thoughts=False, create_label=True)
            print(f"\n{capsule['event_details']}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='event scenario')
    parser.add_argument('--logs', type=str,
                        help="Directory to store the brain log files. Must be specified to persist the log files.")
    args, _ = parser.parse_known_args()

    if args.logs:
        main(Path(args.logs))
    else:
        with TemporaryDirectory(prefix="brain-log") as log_path:
            main(Path(log_path))
