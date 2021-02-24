import pathlib

from leolani.brain.long_term_memory import LongTermMemory
from leolani.brain.utils.base_cases import statements
from pepper.language.generation.thoughts_phrasing import phrase_thoughts
from tests.utils import transform_capsule, random_flags

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    for elem in statements:
        # Create Utterance object
        objects_flag, people_flag, places_flag = random_flags()
        capsule = transform_capsule(elem, objects_flag=objects_flag, people_flag=people_flag,
                                    places_flag=places_flag)

        # Reason about place
        if capsule.context.location.label == capsule.context.location.UNKNOWN:
            potential_location = brain.reason_location(capsule.context)
            if potential_location is not None:
                brain.set_location_label(potential_location)
                capsule.context.location._label = potential_location

        x = brain.update(capsule, reason_types=True)

        print('\n\n---------------------------------------------------------------\n{}\n'.format(capsule.triple))

        try:
            print(('\t\t\tFINAL SAY: ' + phrase_thoughts(x, proactive=True, persist=True)))
        except:
            print(('\t\t\tFINAL SAY: ' + 'No say'))
