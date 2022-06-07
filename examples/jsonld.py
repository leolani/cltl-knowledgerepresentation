"""
THIS SCRIPT GENERATES THE CONTEXT SECTION FOR REPRESENTING DATA IN JSONLD FORMAT.
IT INCLUDES INFORMATION REGARDING THE ONTOLOGIES AND CLASS TYPES USED IN THE BRAIN
"""
import argparse
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from cltl.brain.long_term_memory import LongTermMemory


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    jsonld_path = log_path / 'jsonld'
    os.makedirs(jsonld_path)
    jsonld_filepath = jsonld_path / 'integration_context.jsonld'

    # Create JSONLD context
    jsonld_context = brain.get_jsonld_context(save_path=jsonld_filepath)
    print(jsonld_context)


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
