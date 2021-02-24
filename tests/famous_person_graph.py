# coding=utf-8

import pathlib

from leolani.brain.fame_aware import FameAwareMemory

if __name__ == "__main__":
    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'
    brain = FameAwareMemory(address="http://localhost:7200/repositories/sandbox",
                            log_dir=str(log_path),
                            clear_all=True)

    response = brain.lookup_person_wikidata("Queen Máxima of the Netherlands")
