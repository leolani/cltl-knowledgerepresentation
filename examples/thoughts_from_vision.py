"""
THIS SCRIPT SHOWCASES THE THOUGHTS GENERATED BY THE BRAIN AS AN OBJECT IS IDENTIFIED THROUGH OBJECT RECOGNITION.
THERE ARE 2 TYPES OF THOUGHTS:
4: ENTITY NOVELTY: AWARENESS FOR SUBJECTS OR OBJECTS THAT WERE KNOWN ALREADY
6. OBJECT GAPS: LEARNING OPPORTUNITIES AROUND OBJECTS OF THE STATEMENT
"""

import pathlib

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.base_cases import visuals

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    for detection in visuals:
        # Create experience and get thoughts
        response = brain.get_thoughts_on_entity(detection, reason_types=True)
        print(f'\n\n---------------------------------------------------------------\n{response["triple"]}\n')

        # Show different thoughts
        thoughts = response['thoughts']

        # Completeness thoughts
        print(f'\tobject gaps on {detection}: {thoughts.complement_gaps()}')

        # Engagement
        print(f'\tentity novelty: {thoughts.entity_novelty()}')