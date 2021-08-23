"""
THIS SCRIPT LOOKS FOR A SPECIFIC PERSON AS AN ENTITY IN WIKIDATA AND RETRIEVES ITS 1-HOP GRAPH.
IN THIS SPECIFIC EXAMPLE, IT LOOKS FOR QUEEN MAXIMA OF THE NETHERLANDS
"""

# coding=utf-8


import pathlib

from cltl.brain.fame_aware import FameAwareMemory

if __name__ == "__main__":
    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = FameAwareMemory(address="http://localhost:7200/repositories/sandbox",
                            log_dir=log_path,
                            clear_all=True)

    # Add information to the brain
    response = brain.lookup_person_wikidata("Queen Máxima of the Netherlands")
    print(f'\n\n---------------------------------------------------------------\n{response["data"]}\n')
