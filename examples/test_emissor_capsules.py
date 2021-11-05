

import argparse
import json
from datetime import datetime
from pathlib import Path
from random import getrandbits
from tempfile import TemporaryDirectory

import requests
from pprint import pprint

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import brain_response_to_json
from cltl.combot.backend.api.discrete import UtteranceType

context_id = getrandbits(8)
place_id = getrandbits(8)
location = requests.get("https://ipinfo.io").json()


capsule_post_label = {'chat': '1',
                'turn': '1',
                'author': 'me',
                'utterance': '',
                'utterance_type': UtteranceType.STATEMENT,
                'position': '',
                'subject': {'label': 'Lenka', 'type': ['noun.person']},
                'predicate': {'type': 'label'},
                'object': {'label': 'Lenka', 'type': ['object']},
                'context_id': '1',
                'date': datetime.today(),
                'place': '',
                'place_id': '',
                'country': '',
                'region': '',
                'city': '',
                'objects': [],
                'people': []}

capsule_post = {'chat': '1',
                'turn': '1',
                'author': 'me',
                'utterance': '',
                'utterance_type': UtteranceType.STATEMENT,
                'position': '',
                'subject': {'label': 'Lenka', 'type': ['noun.person']},
                'predicate': {'type': 'like'},
                'object': {'label': 'singing', 'type': ['noun.act']},
                'context_id': '1',
                'date': datetime.today(),
                'place': '',
                'place_id': '',
                'country': '',
                'region': '',
                'city': '',
                'objects': [],
                'people': []}

capsule_query = {'chat': '1',
                'turn': '1',
                'author': 'me',
                'utterance': '',
                'utterance_type': UtteranceType.QUESTION,
                'position': '',
                'subject': {'label': 'lenka', 'type': ['noun.person']},
                'predicate': {'type': 'like'},
                'object': {'label': '', 'type': []},
                'context_id': '1',
                'date': datetime.today(),
                'place': '',
                'place_id': '',
                'country': '',
                'region': '',
                'city': '',
                'objects': [],
                'people': []}



def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)
    data = []
    # Add information to the brain
    response = brain.update(capsule_post_label, reason_types=True, create_label=False)
    print(f"\n\n---------------------------------------------------------------\n{capsule_post_label['triple']}\n")

    #response_json = brain_response_to_json(response)
    #data.append(response_json)
    #pprint(response_json)
    
    answer = brain.query_brain(capsule_query)
    print(f"\n\n---------------------------------------------------------------\n{capsule_query['triple']}\n")

    response_json = brain_response_to_json(answer)
    data.append(response_json)
    pprint(response_json)
    f = open("./capsules/emissor-capsule-responses.json", "w")
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


