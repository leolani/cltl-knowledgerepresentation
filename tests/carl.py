import pathlib

from cltl.brain import LongTermMemory
from tests.utils import transform_capsule, carl

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'

    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=False)
    for elem in carl:

        # Create Utterance object
        capsule = transform_capsule(elem, objects_flag=True, people_flag=True, places_flag=True)
        x = brain.update(capsule, reason_types=True)

        print(f'\n\n---------------------------------------------------------------\n{capsule.triple}\n')
