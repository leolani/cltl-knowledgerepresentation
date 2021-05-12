import pathlib

from leolani.brain import LongTermMemory
from pepper.language.generation.thoughts_phrasing import phrase_thoughts, _phrase_cardinality_conflicts, \
    _phrase_negation_conflicts, _phrase_statement_novelty, _phrase_type_novelty, _phrase_subject_gaps, \
    _phrase_complement_gaps, _phrase_overlaps, _phrase_trust
from tests.utils import transform_capsule, random_flags, capsules

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'leolani' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    for elem in capsules:

        # Create Utterance object
        objects_flag, people_flag, places_flag = random_flags()
        capsule = transform_capsule(elem, objects_flag=objects_flag, people_flag=people_flag,
                                    places_flag=places_flag)

        say = ''
        x = brain.update(capsule, reason_types=True)
        thoughts = x['thoughts']
        utterance = x['statement']

        print('\n\n---------------------------------------------------------------\n{capsule.triple)}\n')

        try:
            print(('\tcardinality conflicts: ' + _phrase_cardinality_conflicts(thoughts.complement_conflicts(),
                                                                               utterance)))
        except:
            print(('\tcardinality conflicts: ' + 'No say'))
        try:
            print(('\tnegation conflicts: ' + _phrase_negation_conflicts(thoughts.negation_conflicts(), utterance)))
        except:
            print(('\tnegation conflicts: ' + 'No say'))
        try:
            print(('\tstatement novelty: ' + _phrase_statement_novelty(thoughts.statement_novelties(), utterance)))
        except:
            print('\tstatement novelty: ' 'No say')
        try:
            print(('\ttype novelty: ' + _phrase_type_novelty(thoughts.entity_novelty(), utterance)))
        except:
            print(('\ttype novelty: ' + 'No say'))
        try:
            print(('\tsubject gaps: ' + _phrase_subject_gaps(thoughts.subject_gaps(), utterance)))
        except:
            print(('\tsubject gaps: ' + 'No say'))
        try:
            print(('\tobject gaps: ' + _phrase_complement_gaps(thoughts.complement_gaps(), utterance)))
        except:
            print(('\tobject gaps: ' + 'No say'))
        try:
            print(('\toverlaps: ' + _phrase_overlaps(thoughts.overlaps(), utterance)))
        except:
            print(('\toverlaps: ' + 'No say'))
        try:
            print(('\ttrust: ' + _phrase_trust(thoughts.trust())))
        except:
            print(('\ttrust: ' + 'No say'))
        try:
            print(('\t\t\tFINAL SAY: ' + phrase_thoughts(x, proactive=True, persist=True)))
        except:
            print(('\t\t\tFINAL SAY: ' + 'No say'))
