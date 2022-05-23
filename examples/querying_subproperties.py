"""
THIS SCRIPT SHOWCASES QUERYING USING INFERENCING. IT TESTS QUERYING THE SUBPROPERTY BE-UNDER BY QUERYING BE-AT.
"""

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
from cltl.commons.discrete import UtteranceType

from cltl.brain.long_term_memory import LongTermMemory

context_id = 12345678
place_id = 87654321
location = requests.get("https://ipinfo.io").json()
start_date = date(2021, 3, 12)

test_context, test_capsules = (
    {"context_id": context_id,
     "date": start_date,
     "place": "Carl's room",
     "place_id": place_id,
     "country": location['country'],
     "region": location['region'],
     "city": location['city']},
    [
        {
            "chat": 1,
            "turn": 1,
            "author": {"label": "leolani", "type": ["robot"], 'uri': "http://cltl.nl/leolani/friends/leolani"},
            "utterance": "I found them. They are under the table.",
            "utterance_type": UtteranceType.STATEMENT,
            "position": "0-25",
            "subject": {"label": "pills", "type": ["object"],
                        'uri': "http://cltl.nl/leolani/world/pills"},
            "predicate": {"label": "be-under",
                          'uri': "http://cltl.nl/leolani/n2mu/be-under"},
            "object": {"label": "table", "type": ["object"],
                       'uri': "http://cltl.nl/leolani/world/table"},
            "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
            "timestamp": datetime.combine(start_date, datetime.now().time()),
            "context_id": context_id
        },
        {
            "chat": 1,
            "turn": 2,
            "author": {"label": "leolani", "type": ["robot"], 'uri': "http://cltl.nl/leolani/friends/leolani"},
            "utterance": "They fell from table.",
            "utterance_type": UtteranceType.STATEMENT,
            "position": "0-21",
            "subject": {"label": "pills", "type": ["object"],
                        'uri': "http://cltl.nl/leolani/world/pills"},
            "predicate": {"label": "fall-from",
                          'uri': "http://cltl.nl/leolani/n2mu/fall-from"},
            "object": {"label": "table", "type": ["object"],
                       'uri': "http://cltl.nl/leolani/world/table"},
            "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
            "timestamp": datetime.combine(start_date, datetime.now().time()),
            "context_id": context_id
        },
        {
            "chat": 1,
            "turn": 3,
            "author": {"label": "carl", "type": ["person"], 'uri': "http://cltl.nl/leolani/friends/carl-1"},
            "utterance": "Where are the pills.",
            "utterance_type": UtteranceType.QUESTION,
            "position": "0-25",
            "subject": {"label": "pills", "type": ["object"],
                        'uri': "http://cltl.nl/leolani/world/pills"},
            "predicate": {"label": "be-at", 'uri': "http://cltl.nl/leolani/n2mu/be-at"},
            "object": {"label": "", "type": [], 'uri': ""},
            "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
            "timestamp": datetime.combine(start_date, datetime.now().time()),
            "context_id": context_id
        },
    ])


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    print(f"\n\n---------------------------------------------------------------\n")
    # Create context
    response = brain.capsule_context(test_context)

    # Add information to the brain
    print(f"\n\n---------------------------------------------------------------\n")
    response = brain.capsule_statement(test_capsules[0], create_label=True)
    print(f"\n{response['statement']['triple']}\n")

    print(f"\n\n---------------------------------------------------------------\n")
    response = brain.capsule_statement(test_capsules[1], create_label=True)
    print(f"\n{response['statement']['triple']}\n")

    print(f"\n\n---------------------------------------------------------------\n")
    response = brain.query_brain(test_capsules[2])
    if response['response']:
        print(f"\n{json.dumps(response['response'], indent=4)}\n")


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
