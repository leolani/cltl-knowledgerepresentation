"""
THIS SCRIPT FILLS IN THE BRAIN WITH A CARL SCENARIO. IN THIS SCENARIO, CARL HAS TO TAKE HIS PILLS BUT CANNOT FIND THEM.
LEOLANI FINDS THEM THROUGH OBJECT RECOGNITION AND COMMUNICATES THIS TO CARL. CARL THEN THANKS LEOLANI
"""
import argparse
from datetime import date
from pathlib import Path
from random import getrandbits
from tempfile import TemporaryDirectory

import requests
from tqdm import tqdm

from cltl.brain.long_term_memory import LongTermMemory
from cltl.combot.backend.api.discrete import UtteranceType

context_id = getrandbits(8)
place_id = getrandbits(8)
location = requests.get("https://ipinfo.io").json()

old_capsule = {
    "chat": 1,
    "turn": 1,
    "author": "carl",
    "utterance": "I did not take my pills.",
    "utterance_type": UtteranceType.STATEMENT,
    "position": "0-25",
    "subject": {"label": "carl", "type": ["person"],
                'uri': "http://cltl.nl/leolani/world/carl-1"},
    "predicate": {"label": "take", "uri": "http://cltl.nl/leolani/n2mu/take"},
    "object": {"label": "pills", "type": ["object", "medicine"],
               'uri': "http://cltl.nl/leolani/world/pills"},
    "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
    "context_id": context_id,
    "date": date(2021, 3, 12),
    "place": "Carl's room",
    "place_id": place_id,
    "country": location['country'],
    "region": location['region'],
    "city": location['city'],
    "objects": [{'type': 'chair', 'confidence': 0.68, 'id': 1}],
    "people": [{'name': 'Carl', 'confidence': 0.94, 'id': 1}]
}

triple_capsule = {
    "chat": 1,
    "turn": 1,
    "author": "carl",
    "utterance": "I did not take my pills.",
    "utterance_type": UtteranceType.STATEMENT,
    "position": "0-25",
    "subject": {"label": "carl", "type": ["person"],
                'uri': "http://cltl.nl/leolani/world/carl-1"},
    "predicate": {"label": "take", "uri": "http://cltl.nl/leolani/n2mu/take"},
    "object": {"label": "pills", "type": ["object", "medicine"],
               'uri': "http://cltl.nl/leolani/world/pills"},
    "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
    "context_id": context_id
}

detection_capsule = {
    "visual": 1,
    "detection": 1,
    "source": "front-camera",
    "image": None,
    "utterance_type": UtteranceType.EXPERIENCE,
    "region": "0-25",
    "objects": [{'type': 'chair', 'confidence': 0.68, 'id': 1}],
    "people": [{'name': 'Carl', 'confidence': 0.94, 'id': 1}],
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
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    response = brain.capsule_context(context_capsule)

    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    response = brain.capsule_detection(detection_capsule)

    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    response = brain.capsule_triple(triple_capsule)


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
