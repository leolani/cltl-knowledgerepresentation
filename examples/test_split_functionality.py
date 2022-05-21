"""
THIS SCRIPT FILLS IN THE BRAIN WITH A CARL SCENARIO. IN THIS SCENARIO, CARL HAS TO TAKE HIS PILLS BUT CANNOT FIND THEM.
LEOLANI FINDS THEM THROUGH OBJECT RECOGNITION AND COMMUNICATES THIS TO CARL. CARL THEN THANKS LEOLANI
"""
import argparse
from datetime import date, datetime
from pathlib import Path
from random import getrandbits
from tempfile import TemporaryDirectory

import requests
from cltl.commons.discrete import UtteranceType

from cltl.brain.long_term_memory import LongTermMemory

context_id = getrandbits(8)
place_id = getrandbits(8)
location = requests.get("https://ipinfo.io").json()

statement_capsule = {
    "chat": 1,
    "turn": 1,
    "author": {"label": "carl", "type": ["person"],
               'uri': "http://cltl.nl/leolani/friends/carl-1"},
    "utterance": "I did not take my pills.",
    "utterance_type": UtteranceType.STATEMENT,
    "position": "0-25",
    "subject": {"label": "carl", "type": ["person"],
                'uri': "http://cltl.nl/leolani/world/carl-1"},
    "predicate": {"label": "take", "uri": "http://cltl.nl/leolani/n2mu/take"},
    "object": {"label": "pills", "type": ["object", "medicine"],
               'uri': "http://cltl.nl/leolani/world/pills"},
    "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
    "timestamp": datetime.now(),
    "context_id": context_id
}

experience_capsule_1 = {
    "visual": 1,
    "detection": 1,
    "source": {"label": "front-camera", "type": ["sensor"],
               'uri': "http://cltl.nl/leolani/inputs/front-camera"},
    "image": None,
    "utterance_type": UtteranceType.EXPERIENCE,
    "region": [752, 46, 1148, 716],
    "item": {'label': 'chair 1', 'type': ['chair'], 'id': 1,
             'uri': "http://cltl.nl/leolani/world/chair-1"},
    'confidence': 0.68,
    "timestamp": datetime.now(),
    "context_id": context_id
}

experience_capsule_2 = {
    "visual": 1,
    "detection": 2,
    "source": {"label": "front-camera", "type": ["sensor"],
               'uri': "http://cltl.nl/leolani/inputs/front-camera"},
    "image": None,
    "utterance_type": UtteranceType.EXPERIENCE,
    "region": [752, 46, 1700, 716],
    "item": {'label': 'Carl', 'type': ['person'], 'id': None,
             'uri': "http://cltl.nl/leolani/world/carl-1"},
    'confidence': 0.94,
    "timestamp": datetime.now(),
    "context_id": context_id
}

mention_capsule_1 = {
    "visual": 1,
    "detection": 3,
    "source": {"label": "front-camera", "type": ["sensor"],
               'uri': "http://cltl.nl/leolani/inputs/front-camera"},
    "image": None,
    "utterance_type": UtteranceType.IMAGE_MENTION,
    "region": [752, 46, 1700, 716],
    "item": {'label': 'Carl', 'type': ['person'], 'id': None,
             'uri': "http://cltl.nl/leolani/world/carl-1"},
    'confidence': 0.94,
    "timestamp": datetime.now(),
    "context_id": context_id
}

mention_capsule_2 = {
    "chat": 1,
    "turn": 1,
    "author": {"label": "carl", "type": ["person"],
               'uri': "http://cltl.nl/leolani/friends/carl-1"},
    "utterance": "I did not take my pills.",
    "utterance_type": UtteranceType.TEXT_MENTION,
    "position": "0-25",
    "item": {'label': 'Carl', 'type': ['person'], 'id': None,
             'uri': "http://cltl.nl/leolani/world/carl-1"},
    'confidence': 0.94,
    "timestamp": datetime.now(),
    "context_id": context_id
}

context_capsule = {
    "context_id": context_id,
    "date": date(2021, 3, 12),  # we take them from the temporal container of scenario
    "place": "Carl's room",
    "place_id": place_id,
    "country": location['country'],
    "region": location['region'],
    "city": location['city']
}


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/leolani",
                           log_dir=log_path,
                           clear_all=True)

    # response = brain.capsule_context(context_capsule)
    #
    # response = brain.capsule_experience(experience_capsule_1)
    #
    # response = brain.capsule_experience(experience_capsule_2)
    #
    # response = brain.capsule_statement(statement_capsule)

    response = brain.capsule_mention(mention_capsule_1)

    response = brain.capsule_mention(mention_capsule_2)

    print('DONE')


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
