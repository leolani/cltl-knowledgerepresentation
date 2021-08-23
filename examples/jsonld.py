"""
THIS SCRIPT GENERATES THE CONTEXT SECTION FOR REPRESENTING DATA IN JSONLD FORMAT.
IT INCLUDES INFORMATION REGARDING THE ONTOLOGIES AND CLASS TYPES USED IN THE BRAIN
"""

import pathlib

from cltl.brain.long_term_memory import LongTermMemory

if __name__ == "__main__":
    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=True)

    # Create JSONLD context
    jsonld_filepath = pathlib.Path.cwd().parent / 'cltl' / 'brain' / 'ontologies' / 'integration_context.jsonld'
    jsonld_context = brain.get_jsonld_context(save_path=jsonld_filepath)

    print(jsonld_context)
