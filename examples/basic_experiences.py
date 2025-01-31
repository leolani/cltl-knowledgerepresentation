"""
THIS SCRIPT FILLS IN THE BRAIN WITH EXPERIENCES,
FOR EXAMPLE, OBSERVING AN OBJECT OR A PERSON.
FOR MORE INFORMATION ON WHAT INFORMATION PLEASE REFER TO cltl.brain.utils.base_cases
"""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from tqdm import tqdm

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.base_cases import experiences, triple_experiences
from cltl.brain.utils.helper_functions import brain_response_to_json


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    data = []
    for (context_capsule, experience_capsules) in tqdm([experiences]):
        print(f"\n\n---------------------------------------------------------------\n")
        # Create context
        response = brain.capsule_context(context_capsule)

        for capsule in experience_capsules:
            # Create experience
            print(f"\n\n---------------------------------------------------------------\n")
            response = brain.capsule_experience(capsule, create_label=True)
            print(f'\n{capsule["entity"]}\n')

            response_json = brain_response_to_json(response)
            data.append(response_json)

    f = open("responses/basic-experiences-responses.json", "w")
    json.dump(data, f)

    for (context_capsule, experience_capsules) in tqdm([triple_experiences]):
        print(f"\n\n---------------------------------------------------------------\n")
        # Create context
        response = brain.capsule_context(context_capsule)

        for capsule in experience_capsules:
            # Create experience
            print(f"\n\n---------------------------------------------------------------\n")
            response = brain.capsule_experience_triple(capsule, reason_types=False, return_thoughts=True, create_label=False)
            print(f'\n{capsule["subject"], capsule["predicate"], capsule["object"]}\n')

            response_json = brain_response_to_json(response)
            data.append(response_json)

    f = open("responses/triple-experiences-responses.json", "w")
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
