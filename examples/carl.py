"""
THIS SCRIPT FILLS IN THE BRAIN WITH A CARL SCENARIO. IN THIS SCENARIO, CARL HAS TO TAKE HIS PILLS BUT CANNOT FIND THEM.
LEOLANI FINDS THEM THROUGH OBJECT RECOGNITION AND COMMUNICATES THIS TO CARL. CARL THEN THANKS LEOLANI
"""
import argparse
import json
from datetime import date, datetime
from pathlib import Path
from random import getrandbits
from tempfile import TemporaryDirectory

import requests
from cltl.commons.discrete import UtteranceType
from tqdm import tqdm

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import brain_response_to_json

context_id = getrandbits(8)
place_id = getrandbits(8)
location = requests.get("https://ipinfo.io").json()
start_date = date(2021, 3, 12)

carl_scenario = ({"context_id": context_id,
                  "date": start_date,
                  "place": "Carl's room",
                  "place_id": place_id,
                  "country": location['country'],
                  "region": location['region'],
                  "city": location['city']},
                 [{
                     "chat": 1,
                     "turn": 1,
                     "author": {"label": "carl", "type": ["person"],
                                'uri': "http://cltl.nl/leolani/friends/carl-1"},
                     "utterance": "I need to take my pills, but I cannot find them.",
                     "utterance_type": UtteranceType.STATEMENT,
                     "position": "0-25",
                     "subject": {"label": "carl", "type": ["person"],
                                 'uri': "http://cltl.nl/leolani/world/carl-1"},
                     "predicate": {"label": "see", "uri": "http://cltl.nl/leolani/n2mu/see"},
                     "object": {"label": "pills", "type": ["object", "medicine"],
                                'uri': "http://cltl.nl/leolani/world/pills"},
                     "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
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
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 1,
                     "detection": 2,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 86, 1148, 816],
                     "item": {'label': 'table 1', 'type': ['table'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/table-1"},
                     'confidence': 0.68,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 1,
                     "detection": 3,
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
                 }, {
                     "chat": 1,
                     "turn": 2,
                     "author": {"label": "leolani", "type": ["robot"],
                                'uri': "http://cltl.nl/leolani/friends/leolani"},
                     "utterance": "I found them. They are under the table.",
                     "utterance_type": UtteranceType.STATEMENT,
                     "position": "0-25",
                     "subject": {"label": "pills", "type": ["object"], 'uri': "http://cltl.nl/leolani/world/pills"},
                     "predicate": {"label": "located under", "uri": "http://cltl.nl/leolani/n2mu/located-under"},
                     "object": {"label": "table", "type": ["object"], 'uri': "http://cltl.nl/leolani/world/table"},
                     "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 2,
                     "detection": 1,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1148, 716],
                     "item": {'label': 'chair 1', 'type': ['chair'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/chair-1"},
                     'confidence': 0.56,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 2,
                     "detection": 2,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1148, 716],
                     "item": {'label': 'table 1', 'type': ['table'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/table-1"},
                     'confidence': 0.87,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 2,
                     "detection": 3,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1148, 716],
                     "item": {'label': 'pillbox 1', 'type': ['pillbox'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/pillbox-1"},
                     'confidence': 0.92,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "chat": 1,
                     "turn": 3,
                     "author": {"label": "carl", "type": ["person"],
                                'uri': "http://cltl.nl/leolani/friends/carl-1"},
                     "utterance": "Oh! Got it. Thank you.",
                     "utterance_type": UtteranceType.STATEMENT,
                     "position": "0-25",
                     "subject": {"label": "carl", "type": ["person"], 'uri': "http://cltl.nl/leolani/world/carl-1"},
                     "predicate": {"label": "see", "uri": "http://cltl.nl/leolani/n2mu/see"},
                     "object": {"label": "pills", "type": ["object"], 'uri': "http://cltl.nl/leolani/world/pills"},
                     "perspective": {"certainty": 1, "polarity": 1, "sentiment": 1},
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id,
                 }, {
                     "visual": 3,
                     "detection": 1,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1148, 716],
                     "item": {'label': 'chair 1', 'type': ['chair'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/chair-1"},
                     'confidence': 0.59,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 3,
                     "detection": 2,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1148, 716],
                     "item": {'label': 'table 1', 'type': ['table'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/table-1"},
                     'confidence': 0.73,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 3,
                     "detection": 3,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1148, 716],
                     "item": {'label': 'pillbox 1', 'type': ['pillbox'], 'id': 1,
                              'uri': "http://cltl.nl/leolani/world/pillbox-1"},
                     'confidence': 0.79,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     "visual": 3,
                     "detection": 4,
                     "source": {"label": "front-camera", "type": ["sensor"],
                                'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                     "image": None,
                     "utterance_type": UtteranceType.EXPERIENCE,
                     "region": [752, 46, 1700, 716],
                     "item": {'label': 'Carl', 'type': ['person'], 'id': None,
                              'uri': "http://cltl.nl/leolani/world/carl-1"},
                     'confidence': 0.98,
                     "timestamp": datetime.combine(start_date, datetime.now().time()),
                     "context_id": context_id
                 }, {
                     'chat': '1',
                     'turn': '5',
                     "author": {"label": "carl", "type": ["person"],
                                'uri': "http://cltl.nl/leolani/friends/carl-1"},
                     'utterance': '',
                     'position': '0 - 32',
                     'item': {'label': 'Tom', 'type': ['person'],
                              'id': None, 'uri': 'http://cltl.nl/leolani/world/tom-1'},
                     'perspective': {
                         'emotion': 'EmotionType.GO:joy',
                         'confidence': 0.724881649017334
                     },
                     'context_id': context_id,
                     'timestamp': datetime.combine(start_date, datetime.now().time()),
                     'utterance_type': UtteranceType.TEXT_ATTRIBUTION
                 }
                 ]
                 )


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)
    data = []
    for (context_capsule, content_capsules) in tqdm([carl_scenario]):
        print(f"\n\n---------------------------------------------------------------\n")
        # Create context
        response = brain.capsule_context(context_capsule)

        for capsule in content_capsules:
            # Add information to the brain
            if capsule['utterance_type'] == UtteranceType.STATEMENT:
                response = brain.capsule_statement(capsule, reason_types=True, create_label=True)
                print(f"\n{capsule['triple']}\n")
            if capsule['utterance_type'] == UtteranceType.EXPERIENCE:
                response = brain.capsule_experience(capsule, create_label=True)
                print(f"\n{capsule['entity']}\n")

            if capsule['utterance_type'] in (UtteranceType.IMAGE_MENTION, UtteranceType.TEXT_MENTION,
                                             UtteranceType.TEXT_ATTRIBUTION, UtteranceType.IMAGE_ATTRIBUTION):
                response = brain.capsule_mention(capsule, create_label=True)
                print(f"\n{capsule['entity']}\n")

            response_json = brain_response_to_json(response)
            data.append(response_json)

    f = open("responses/carl-responses.json", "w")
    json.dump(data, f)


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
