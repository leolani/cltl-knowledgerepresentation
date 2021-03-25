import pathlib
import json

from leolani.brain import LongTermMemory

if __name__ == "__main__":
    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'

    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    jsonld_filepath = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'ontologies' / 'integration_context.jsonld'
    final = brain.get_jsonld_context(save_path=jsonld_filepath)

    print("done")
