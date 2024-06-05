import enum
import pathlib
from datetime import date

import importlib_resources as pkg_resources
import numpy as np
from cltl.commons.casefolding import casefold_text
from cltl.commons.discrete import Certainty, Polarity, Sentiment, Emotion
from rdflib import URIRef, Literal

import cltl.brain
from cltl.brain.utils.constants import CAPITALIZED_TYPES


def read_query(query_filename):
    """
    Read a query from file and return as a string
    Parameters
    ----------
    query_filename: str name of the query. It will be looked for in the queries folder of this project

    Returns
    -------
    query: str the query with placeholders for the query parameters, as a string to be formatted

    """
    resources = pkg_resources.files(cltl.brain)

    return (resources / "queries" / f"{query_filename}.rq").read_text()


def is_proper_noun(types):
    return any(i in types for i in CAPITALIZED_TYPES)


def remove_articles(text):
    articles = ['a-', 'this-', 'the-']
    for a in articles:
        if text.startswith(a):
            text = text.replace(a, '')
    return text


def date_from_uri(uri):
    [year, month, day] = uri.split('/')[-1].split('-')
    return date(int(year), int(month), int(day))


def hash_claim_id(triple):
    return '_'.join(triple)


def confidence_to_certainty_value(confidence):
    return Certainty.as_enum(confidence)


def polarity_to_polarity_value(polarity):
    return Polarity.as_enum(polarity)


def sentiment_to_sentiment_value(sentiment):
    return Sentiment.as_enum(sentiment)


def emotion_to_emotion_value(emotion):
    return Emotion.as_enum(emotion)


def replace_in_file(file, word, word_replacement):
    for i, line in enumerate(open(file)):
        line.replace(':%s' % word, ':%s' % word_replacement)
        line.replace('"%s' % word, '"%s' % word_replacement)


def get_object_id(memory, category):
    cat_mem = memory.get(casefold_text(category, format='triple'), {'brain_ids': [], 'local_ids': [], 'ids': []})
    l = cat_mem['ids'][:]
    id = l[0]
    tail = l[1:]

    cat_mem['ids'] = tail
    memory[casefold_text(category, format='triple')] = cat_mem
    return id, memory


def sigmoid(z, growth_rate=1):
    return 1 / (1 + np.exp(-z * growth_rate))


def element_to_json(v):
    if type(v) in [str, int, float, bool, np.float64] or v is None:
        pass
    elif isinstance(v, (URIRef, Literal, pathlib.Path)):
        v = str(v)
    elif isinstance(v, date):
        v = v.isoformat()
    elif isinstance(v, enum.Enum):
        v = v.name
    elif isinstance(v, list) or isinstance(v, tuple):
        v = [element_to_json(el) for el in v]
    elif isinstance(v, dict):
        v = {inner_k: element_to_json(inner_v) for inner_k, inner_v in v.items()}
    else:
        v = {inner_k: element_to_json(inner_v) for inner_k, inner_v in v.__dict__.items()}

    return v


def brain_response_to_json(capsule):
    return {k: element_to_json(v) for k, v in capsule.items()}
