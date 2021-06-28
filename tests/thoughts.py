import pathlib

from cltl.brain import LongTermMemory
from utils import transform_capsule, capsules

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=False)

    for capsule in capsules:

        # Create Utterance object, with random context
        utterance = transform_capsule(capsule)

        # Add information to the brain
        response = brain.update(utterance, reason_types=True)
        print(f'\n\n---------------------------------------------------------------\n{utterance.triple}\n')

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
            print(f'\ttrust on {utterance.chat_speaker}: {thoughts.trust()}')
        except:
            print(f'\ttrust: No say')
