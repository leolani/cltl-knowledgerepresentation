"""
THIS SCRIPT FILLS IN THE BRAIN WITH THE CAPSULES SAVED IN A GIVEN JSON FILE
"""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import brain_response_to_json


def main(log_path):
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=True)
    # Read json
    f = open("capsules/baking.json", "r")
    [context_capsule, statements_capsules] = json.load(f)

    # Create context
    response = brain.capsule_context(context_capsule)

    data = []
    for capsule in statements_capsules:
        # Add information to the brain
        if capsule['utterance_type'] == "STATEMENT":
            brain_response = brain.capsule_statement(capsule, reason_types=True, create_label=True)
            print(f"\n{capsule['triple']}\n")
        elif capsule['utterance_type'] == "EXPERIENCE":
            brain_response = brain.capsule_experience(capsule, create_label=True)
            print(f"\n{capsule['triple']}\n")
        elif capsule['utterance_type'] in ("IMAGE_MENTION", "TEXT_MENTION", "TEXT_ATTRIBUTION", "IMAGE_ATTRIBUTION"):
            brain_response = brain.capsule_mention(capsule, create_label=True)
            print(f"\n{capsule['triple']}\n")
        elif capsule['utterance_type'] == "QUESTION":
            brain_response = brain.query_brain(capsule)
            print(f"\n{capsule['triple']}\n")
        else:
            brain_response = {}
            print(f"Skipped capsule utterance type: {capsule['utterance_type']}")

        response_json = brain_response_to_json(brain_response)
        data.append(response_json)

    f = open("responses/basic-statements-responses.json", "w")
    json.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Carl-Leolani scenario')
    parser.add_argument('--logs', type=str,
                        help="Directory to store the brain log files. Must be specified to persist the log files.")
    args, _ = parser.parse_known_args()

    if args.logs:
        main(Path(args.logs))
    else:
        with TemporaryDirectory(prefix="brain-log") as log_path:
            main(Path(log_path))
