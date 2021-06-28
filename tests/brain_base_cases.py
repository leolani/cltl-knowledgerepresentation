import pathlib

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.base_cases import statements
from utils import transform_capsule

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    for statement in statements:
        # Create Utterance object, with random context
        utterance = transform_capsule(statement)

        # Add information to the brain
        response = brain.update(utterance, reason_types=True)
        print(f'\n\n---------------------------------------------------------------\n{utterance.triple}\n')
