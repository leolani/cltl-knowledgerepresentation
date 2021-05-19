import pathlib
from datetime import date

from cltl.brain import LongTermMemory
from tests.utils import transform_capsule

carl_scenario = [
    {
        "utterance": "I need to take my pills, but I cannot find them.",
        # sequence of mention (derived from container in mention)
        "subject": {"label": "carl", "type": "person"},  # annotations of type NER
        "predicate": {"type": "sees"},  # annotation of type x (still to be done)
        "object": {"label": "pills", "type": "object"},  # annotations of type NER
        "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},  # annotation of type x (still to be done)
        "author": "carl",  # speaker of scenario (maybe we want to change this)
        "chat": 1,  # segment of text signal
        "turn": 1,  # segment of text signal
        "position": "0-25",  # segment of the annotation
        "date": date(2021, 3, 12),  # we take them from the temporal container of scenario
        "objects": [('chair', 0.79)],  # Usually come from Vision, for now we take them from scenario['context']
        "people": [('chair', 0.79)],  # Usually come from Vision, for now we take them from scenario['context']
        "place": ""
    },
    {
        "utterance": "I found them. They are under the table.",
        "subject": {"label": "pills", "type": "object"},
        "predicate": {"type": "locatedUnder"},
        "object": {"label": "table", "type": "object"},
        "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
        "author": "leolani",
        "chat": 1,
        "turn": 2,
        "position": "0-25",
        "date": date(2021, 3, 12)
    },
    {
        "utterance": "Oh! Got it. Thank you.",
        "subject": {"label": "carl", "type": "person"},
        "predicate": {"type": "sees"},
        "object": {"label": "pills", "type": "object"},
        "perspective": {"certainty": 1, "polarity": 1, "sentiment": 1},
        "author": "carl",
        "chat": 1,
        "turn": 3,
        "position": "0-25",
        "date": date(2021, 3, 12)
    }
]

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'

    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=False)
    for capsule in carl_scenario:
        # Create Utterance object
        utterance = transform_capsule(capsule, objects_flag=True, people_flag=True, places_flag=True)
        x = brain.update(utterance, reason_types=True)

        print(f'\n\n---------------------------------------------------------------\n{utterance.triple}\n')
