"""TODO: DOCUMENT THIS SCRIPT."""
# coding=utf-8

import pathlib

from cltl.brain.fame_aware import FameAwareMemory

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = FameAwareMemory(address="http://localhost:7200/repositories/sandbox",
                            log_dir=str(log_path),
                            clear_all=True)

    # Add information to the brain
    response = brain.lookup_person_wikidata("Queen Máxima of the Netherlands")
    print(f'\n\n---------------------------------------------------------------\n{response["data"]}\n')
