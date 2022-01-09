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
                      'subject': {'label': 'Lenka', 'type': ['noun.person'],
                                  "uri": "http://cltl.nl/leolani/world/lenka"},
                      'predicate': {'label': 'label', 'uri': 'http://cltl.nl/leolani/n2mu/label'},
                      'object': {'label': 'Lenka', 'type': ['object'], "uri": "http://cltl.nl/leolani/world/lenka"},
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
                'subject': {'label': 'Lenka', 'type': ['noun.person'], "uri": "http://cltl.nl/leolani/world/lenka"},
                'predicate': {'label': 'like', 'uri': 'http://cltl.nl/leolani/n2mu/like'},
                'object': {'label': 'singing', 'type': ['noun.act'], "uri": "http://cltl.nl/leolani/world/singing"},
                'context_id': '1',
                'date': datetime.today(),
                'place': '',
                'place_id': '',
                'country': '',
                'region': '',
                'city': '',
                'objects': [],
                'people': []}

capsule_post_label2 = {'author': 'Fred',
                       'certainty': 1,
                       'chat': '2021-11-12-15:44:22',
                       'city': 'Amsterdam',
                       'context_id': 'Leolani2',
                       'country': 'NL',
                       'date': datetime.today(),
                       'object': {'label': 'pizza', 'type': ['noun.food'], "uri": "http://cltl.nl/leolani/world/pizza"},
                       'objects': [],
                       'people': [],
                       'place': 'Amsterdam',
                       'place_id': 116,
                       'polarity': 1,
                       'position': '0-12',
                       'predicate': {'label': 'like', 'type': 'verb.emotion', 'uri': 'http://cltl.nl/leolani/n2mu/like', 'type': 'verb.emotion'},
                       'region': 'North Holland',
                       'sentiment': '0.75',
                       'subject': {'label': 'Fred', 'type': ['person'], "uri": "http://cltl.nl/leolani/world/fred"},
                       'turn': '28cbc878-6a52-4b7e-a5b9-b81ffe295c9f',
                       'utterance': 'I like pizza',
                       'utterance_type': UtteranceType.STATEMENT}

capsule_query = {'chat': '1',
                 'turn': '1',
                 'author': 'me',
                 'utterance': '',
                 'utterance_type': UtteranceType.QUESTION,
                 'position': '',
                 'subject': {'label': 'fred', 'type': ['noun.person'], "uri": "http://cltl.nl/leolani/world/fred"},
                 'predicate': {'label': 'like', 'uri': 'http://cltl.nl/leolani/n2mu/like'},
                 'object': {'label': '', 'type': [], "uri": ""},
                 'context_id': '1',
                 'date': datetime.today(),
                 'place': '',
                 'place_id': '',
                 'country': '',
                 'region': '',
                 'city': '',
                 'objects': [],
                 'people': []}

test_capsule = {'author': 'Piek_t_139219',
                'chat': '2021-11-11-19:41:23',
                'city': 'Amsterdam',
                'context_id': 'Leolani2',
                'country': 'NL',
                'date': datetime.today(),
                'object': {'label': '', 'type': [], "uri": ""},
                'objects': [{'confidence': 0.59, 'id': 1, 'type': 'chair'},
                            {'confidence': 0.73, 'id': 1, 'type': 'table'},
                            {'confidence': 0.32, 'id': 1, 'type': 'pillbox'}],
                'people': [{'confidence': 0.98, 'id': 1, 'name': 'Piek_t_139219'}],
                'perspective': None,
                'place': 'Amsterdam',
                'place_id': 64,
                'position': '0-19',
                'predicate': {'label': 'fred-is', 'uri': 'http://cltl.nl/leolani/n2mu/fred-is'},
                'region': 'North Holland',
                'subject': {'label': 'does', 'type': ['verb.social'], "uri": "http://cltl.nl/leolani/world/does"},
                'turn': '31efe544-6876-417c-9c44-0f554e23debf',
                'utterance': 'What does fred like',
                'utterance_type': UtteranceType.QUESTION
                }


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)
    data = []
    # Add information to the brain
    response = brain.update(capsule_post_label2, reason_types=True, create_label=False)

    response_json = brain_response_to_json(response)
    # data.append(response_json)
    pprint(response_json)

    answer = brain.query_brain(test_capsule)

    # response_json = brain_response_to_json(answer)
    # data.append(response_json)
    # pprint(response_json)
    # f = open("./capsules/emissor-capsule-responses.json", "w")
    # json.dump(data, f)


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