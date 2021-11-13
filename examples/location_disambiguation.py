"""
THIS SCRIPT SHOWS THE CAPABILITIES FOR IDENTIFYING A LOCATION. IT CONTAINS THREE USE CASES,
FIRST A KNOWN PLACE WITH A LABEL WHERE NO REASONING IS NEEDED.
SECOND, AN UNKNOWN PLACE WITHOUT LABEL. FOR SHOWCASING PURPOSES WE ASSIGN A RANDOM LABEL
    AND SET THE NAME CORRECTLY IN THE BRAIN
THIRD, A KNOWN LOCATION WITHOUT A LABEL (A NON RECOGNIZED PLACE). THROUGH REASONING THIS PLACE IS RECOGNIZED
    AND THE NAME IS SET CORRECTLY IN THE BRAIN
"""
import argparse
from datetime import date
from pathlib import Path
from random import choice
from random import getrandbits
from tempfile import TemporaryDirectory

import requests
from tqdm import tqdm

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.base_cases import places
from cltl.combot.backend.api.discrete import UtteranceType

place_id = getrandbits(8)
location = requests.get("https://ipinfo.io").json()

unknown_location_scenario = [
    {  # Known place
        "chat": 100,
        "turn": 6,
        "author": "tae",
        "utterance": "I do not eat beef",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-19",
        "subject": {"label": "tae", "type": ["person"]},
        "predicate": {"label": "eat"},
        "object": {"label": "beef", "type": ["food"]},
        "perspective": {"certainty": 1, "polarity": -1, "sentiment": 1},
        "context_id": getrandbits(8),
        "date": date(2020, 9, 29),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [{'type': 'chair', 'confidence': 0.59, 'id': 1},
                    {'type': 'table', 'confidence': 0.73, 'id': 1},
                    {'type': 'chair', 'confidence': 0.82, 'id': 2}],
        "people": []},
    {  # Unknown (new) place,
        "chat": 101,
        "turn": 1,
        "author": "selene",
        "utterance": "I am hungry",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-11",
        "subject": {"label": "selene", "type": ["person"]},
        "predicate": {"label": "be"},
        "object": {"label": "hungry", "type": [""]},
        "perspective": {"certainty": 1, "polarity": 1, "sentiment": -1},
        "context_id": getrandbits(8),
        "date": date(2021, 2, 18),
        "place": None,
        "place_id": None,
        "country": location['country'],
        "region": location['region'],
        "city": location['city'],
        "objects": [{'type': 'apple', 'confidence': 0.59, 'id': 1},
                    {'type': 'orange', 'confidence': 0.73, 'id': 1},
                    {'type': 'avocado', 'confidence': 0.82, 'id': 2}],
        "people": [{'name': 'Selene', 'confidence': 0.98, 'id': 1}]
    },
    {  # Known place but not recognized,
        "chat": 102,
        "turn": 1,
        "author": "piek",
        "utterance": "I am busy",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-9",
        "subject": {"label": "piek", "type": ["person"]},
        "predicate": {"label": "be"},
        "object": {"label": "busy", "type": [""]},
        "perspective": {"certainty": 1, "polarity": 1, "sentiment": -1},
        "context_id": getrandbits(8),
        "date": date(2021, 7, 6),
        "place": None,
        "place_id": None,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [{'type': 'chair', 'confidence': 0.59, 'id': 1},
                    {'type': 'table', 'confidence': 0.73, 'id': 1},
                    {'type': 'chair', 'confidence': 0.82, 'id': 2}],
        "people": [{'name': 'Selene', 'confidence': 0.98, 'id': 1}]
    },
]


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=True)

    for capsule in tqdm(unknown_location_scenario):
        # Reason about location
        if capsule['place'] is None or capsule['place'].lower() == '':
            potential_location = brain.reason_location(capsule)

            if potential_location:
                # Success
                capsule['place'] = potential_location
                say = 'Having a talk at what I figured out is %s' % capsule['place']

                # Add information to the brain
                response = brain.update(capsule, reason_types=True, create_label=True)

                # Set the location name
                brain.set_location_label(capsule['context_id'], capsule['place'])
            else:
                # Add information to the brain
                response = brain.update(capsule, reason_types=True, create_label=True)

                # Failed to reason, select a random place
                place = choice(places)
                capsule['place'] = place
                say = 'I could not figure out where I am, so I will randomly call it %s' % capsule['place']

                # Set the location name
                brain.set_location_label(capsule['context_id'], capsule['place'])

        else:
            # Add information to the brain
            response = brain.update(capsule, reason_types=True, create_label=True)

            say = 'I know I am at %s' % capsule['place']

        print(say)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Carl-Leolani scenario')
    parser.add_argument('--logs', type=str,
                        help="Directory to store the brain log files. Must be specified to persist the log files.")
    args, _ = parser.parse_known_args()

    if args.logs:
        main(Path(args.logs))
    else:
        with TemporaryDirectory(prefix="brain-log") as log_path:
            main(Path(log_path))
