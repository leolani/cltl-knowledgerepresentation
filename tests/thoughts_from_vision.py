import pathlib

from leolani.brain.long_term_memory import LongTermMemory
from leolani.brain.utils.base_cases import visuals, experiences
from pepper.language.generation.thoughts_phrasing import phrase_thoughts
from tests.utils import transform_capsule, random_flags

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    flat_list = [item for detection in visuals for item in detection]
    unique_detections = set(flat_list)
    template = experiences[0]

    for elem in unique_detections:
        # Create experience and get thoughts
        x = brain.get_thoughts_on_entity(elem, reason_types=True)

        # Use experience template as phrasing requires an utterance object
        # TODO: remove undesired dependency
        template['object']['label'] = x['entity'].label
        template['object']['type'] = x['entity'].types_names

        objects_flag, people_flag, places_flag = random_flags()
        capsule = transform_capsule(template, objects_flag=objects_flag, people_flag=people_flag,
                                    places_flag=places_flag)
        x['statement'] = capsule

        # Phrase thoughts

        print('\n\n---------------------------------------------------------------\n{}\n'.format(capsule.triple))

        try:
            print(('\t\t\tFINAL SAY: ' + phrase_thoughts(x, entity_only=True, proactive=True, persist=True)))
        except:
            print(('\t\t\tFINAL SAY: ' + 'No say'))
