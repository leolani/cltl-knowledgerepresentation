import pathlib
from datetime import date
from random import getrandbits

import requests

from cltl.brain import LongTermMemory
from cltl.combot.backend.api.discrete import UtteranceType
from utils import transform_capsule

context_id = getrandbits(8)
place_id = getrandbits(8)
location = requests.get("https://ipinfo.io").json()

carl_scenario = [
    {
        "chat": 1,  # segment of text signal
        "turn": 1,  # segment of text signal
        "author": "carl",  # speaker of scenario
        "utterance": "I need to take my pills, but I cannot find them.",  # sequence of mention
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",  # segment of the annotation
        "subject": {"label": "carl", "type": "person"},  # annotations of type NER
        "predicate": {"type": "sees"},  # annotation of type x (still to be done)
        "object": {"label": "pills", "type": "object"},  # annotations of type NER
        "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},  # annotation of type x (still to be done)
        "context_id": context_id,
        "date": date(2021, 3, 12),  # we take them from the temporal container of scenario
        "place": "Carl's room",
        "place_id": place_id,
        "country": location['country'],
        "region": location['region'],
        "city": location['city'],
        "objects": [{'type': 'chair', 'confidence': 0.68, 'id': 1},
                    {'type': 'table', 'confidence': 0.79, 'id': 1}],  # Usually come from Vision
        "people": [{'name': 'Carl', 'confidence': 0.94, 'id': 1}]  # Usually come from Vision
    },
    {
        "chat": 1,
        "turn": 2,
        "author": "leolani",
        "utterance": "I found them. They are under the table.",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {"label": "pills", "type": "object"},
        "predicate": {"type": "located under"},
        "object": {"label": "table", "type": "object"},
        "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
        "context_id": context_id,
        "date": date(2021, 3, 12),
        "place": "Carl's room",
        "place_id": place_id,
        "country": location['country'],
        "region": location['region'],
        "city": location['city'],
        "objects": [{'type': 'chair', 'confidence': 0.56, 'id': 1},
                    {'type': 'table', 'confidence': 0.87, 'id': 1},
                    {'type': 'pillbox', 'confidence': 0.92, 'id': 1}],
        "people": []
    },
    {
        "chat": 1,
        "turn": 3,
        "author": "carl",
        "utterance": "Oh! Got it. Thank you.",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {"label": "carl", "type": "person"},
        "predicate": {"type": "sees"},
        "object": {"label": "pills", "type": "object"},
        "perspective": {"certainty": 1, "polarity": 1, "sentiment": 1},
        "context_id": context_id,
        "date": date(2021, 3, 12),
        "place": "Carl's room",
        "place_id": place_id,
        "country": location['country'],
        "region": location['region'],
        "city": location['city'],
        "objects": [{'type': 'chair', 'confidence': 0.59, 'id': 1},
                    {'type': 'table', 'confidence': 0.73, 'id': 1},
                    {'type': 'pillbox', 'confidence': 0.32, 'id': 1}],
        "people": [{'name': 'Carl', 'confidence': 0.98, 'id': 1}]
    }
]

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=True)

    for capsule in carl_scenario:
        # Create Utterance object
        utterance = transform_capsule(capsule)

        # Add information to the brain
        response = brain.update(capsule, reason_types=True)
        print(f'\n\n---------------------------------------------------------------\n{utterance.triple}\n')
