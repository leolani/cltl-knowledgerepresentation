import pathlib

from cltl.brain import LongTermMemory

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    # Create JSONLD context
    jsonld_filepath = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'ontologies' / 'integration_context.jsonld'
    final = brain.get_jsonld_context(save_path=jsonld_filepath)

    print("done")
