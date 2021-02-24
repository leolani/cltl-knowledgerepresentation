import pathlib

from leolani.brain import LongTermMemory
from tests.utils import random_flags, transform_capsule, fake_place, capsules

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    for capsule in capsules:
        say = ''
        objects_flag, people_flag, places_flag = random_flags()
        capsule = transform_capsule(capsule, objects_flag=objects_flag, people_flag=people_flag,
                                    places_flag=places_flag)

        x = brain.update(capsule, reason_types=True)

        # Reason about location
        if capsule.context.location.label == capsule.context.location.UNKNOWN:
            potential_location = brain.reason_location(capsule.context)

            if potential_location:
                # Success, set the location name
                brain.set_location_label(potential_location)
                capsule.context.location.label = potential_location
                say += 'Having a talk at what I figured out is %s' % capsule.context.location.label
            else:
                # Failed to reason, select a random place
                place = fake_place()
                brain.set_location_label(place)
                capsule.context.location.label = place
                say += 'I could not figure out where I am, so I will randomly call it %s' % capsule.context.location.label

        else:
            say += 'I know I am at %s' % capsule.context.location.label
        print(say)
