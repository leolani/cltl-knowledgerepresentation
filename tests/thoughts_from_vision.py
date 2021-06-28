import pathlib

from cltl.brain.long_term_memory import LongTermMemory
from tests.utils import unique_detections

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=False)

    for detection in unique_detections:
        # Create experience and get thoughts
        response = brain.get_thoughts_on_entity(detection, reason_types=True)
        print(f'\n\n---------------------------------------------------------------\n{response["triple"]}\n')

        # Show different thoughts
        thoughts = response['thoughts']
        try:
            print(f'\tcardinality conflicts: {thoughts.complement_conflicts()}')
        except:
            print('\tcardinality conflicts: No say')
        try:
            print(f'\tnegation conflicts: {thoughts.negation_conflicts()}')
        except:
            print(f'\tnegation conflicts: No say')
        try:
            print(f'\tstatement novelty: {thoughts.statement_novelties()}')
        except:
            print(f'\tstatement novelty: ' 'No say')
        try:
            print(f'\ttype novelty: {thoughts.entity_novelty()}')
        except:
            print(f'\ttype novelty: No say')
        try:
            print(f'\tsubject gaps: {thoughts.subject_gaps()}')
        except:
            print(f'\tsubject gaps: No say')
        try:
            print(f'\tobject gaps: {thoughts.complement_gaps()}')
        except:
            print(f'\tobject gaps: No say')
        try:
            print(f'\toverlaps: {thoughts.overlaps()}')
        except:
            print(f'\toverlaps: No say')
        try:
            print(f'\ttrust: {thoughts.trust()}')
        except:
            print(f'\ttrust: No say')
