"""
THIS SCRIPT LOOKS FOR A SPECIFIC PERSON AS AN ENTITY IN WIKIDATA AND RETRIEVES ITS 1-HOP GRAPH.
IN THIS SPECIFIC EXAMPLE, IT LOOKS FOR QUEEN MAXIMA OF THE NETHERLANDS
"""

# coding=utf-8
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from cltl.brain.fame_aware import FameAwareMemory


def main(log_path):
    # Create brain connection
    brain = FameAwareMemory(address="http://localhost:7200/repositories/sandbox",
                            log_dir=log_path,
                            clear_all=False)
    # Add information to the brain
    response = brain.lookup_person_wikidata("Queen Máxima of the Netherlands")
    print(f'\n{response["data"]}')


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
