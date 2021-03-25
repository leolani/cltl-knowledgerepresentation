import pathlib

from leolani.brain import LongTermMemory
from tests.utils import transform_capsule, carl

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'

    for elem in carl:
        brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                               log_dir=str(log_path),
                               clear_all=False)

        # Create Utterance object
        capsule = transform_capsule(elem, objects_flag=True, people_flag=True, places_flag=True)

        say = ''
        x = brain.update(capsule, reason_types=True)
        thoughts = x['thoughts']
        utterance = x['statement']

        print('\n\n---------------------------------------------------------------\n{}\n'.format(capsule.triple))
