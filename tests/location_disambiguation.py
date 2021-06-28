import pathlib
from random import choice

from cltl.brain import LongTermMemory
from utils import transform_capsule, places, capsules

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=False)

    for capsule in capsules:

        # Create Utterance object, with random context
        capsule = transform_capsule(capsule)
        # Add information to the brain
        response = brain.update(capsule, reason_types=True)

        # Reason about location
        if capsule.context.location.label == capsule.context.location.UNKNOWN:
            potential_location = brain.reason_location(capsule.context)

            if potential_location:
                # Success, set the location name
                brain.set_location_label(potential_location)
                capsule.context.location.label = potential_location
                say = 'Having a talk at what I figured out is %s' % capsule.context.location.label
            else:
                # Failed to reason, select a random place
                place = choice(places)
                brain.set_location_label(place)
                capsule.context.location.label = place
                say = 'I could not figure out where I am, so I will randomly call it %s' % capsule.context.location.label

        else:
            say = 'I know I am at %s' % capsule.context.location.label
        print(say)
