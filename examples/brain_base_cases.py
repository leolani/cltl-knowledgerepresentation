"""
THIS SCRIPT FILLS IN THE BRAIN WITH BASIC INFORMATION REGARDING EACH OF THE TEAM'S DEVELOPERS,
FOR EXAMPLE, WHERE THEY ARE FROM, WHAT THEY LIKE, AND WHERE THEY LIVE.
FOR MORE INFORMATION ON WHAT INFORMATION PLEASE REFER TO cltl.brain.utils.base_cases
"""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

import json
from tqdm import tqdm

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import brain_response_to_json
from cltl.brain.utils.base_cases import statements


def main(log_path):
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=True)
    data = []
    for statement in tqdm(statements):
        # Add information to the brain
        response = brain.update(statement, reason_types=True, create_label=True)
        print(f"\n{statement['triple']}\n---------------------------------------------------------------\n\n")

        response_json = brain_response_to_json(response)
        data.append(response_json)

    # f = open("../../cltl-languagegeneration/examples/data/base-case-responses.json", "w")
    # json.dump(data, f)


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
