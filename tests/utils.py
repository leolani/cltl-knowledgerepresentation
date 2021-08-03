from datetime import date
from random import choice, sample, randint, uniform

import numpy as np

from cltl.brain import RdfBuilder, Perspective
from cltl.brain.utils.base_cases import visuals
from cltl.combot.backend.api.discrete import UtteranceType, Emotion
from cltl.combot.infra.util import Bounds
from brain_external import Context, Face, Object, Chat, Utterance, UtteranceHypothesis

TEST_IMG = np.zeros((128,))
TEST_BOUNDS = Bounds(0.0, 0.0, 0.5, 1.0)

name = 'Leolani'
places = ['Forest', 'Playground', 'Monastery', 'House', 'University', 'Hotel', 'Office']
friends = ['Piek', 'Lenka', 'Bram', 'Suzana', 'Selene', 'Lea', 'Thomas', 'Jaap', 'Tae']
unique_detections = set([item for detection in visuals for item in detection])

binary_values = [True, False]

capsule_knows = {
    "utterance": "Bram knows Lenka",
    "subject": {"label": "bram", "type": "person"},
    "predicate": {"type": "know"},
    "object": {"label": "lenka", "type": "person"},
    "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
    "author": "suzana",
    "chat": 6,
    "turn": 4,
    "position": "0-16",
    "date": date(2019, 3, 19)
}

capsule_is_from = {
    "utterance": "Lenka is from Serbia",
    "subject": {"label": "lenka", "type": "person"},
    "predicate": {"type": "be-from"},
    "object": {"label": "serbia", "type": "location"},
    "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
    "author": "piek",
    "chat": 1,
    "turn": 1,
    "position": "0-25",
    "date": date(2017, 10, 24)
}

capsule_is_from_2 = {
    "utterance": "Bram is from the Netherlands",
    "subject": {"label": "bram", "type": "person"},
    "predicate": {"type": "be-from"},
    "object": {"label": "netherlands", "type": "location"},
    "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
    "author": "piek",
    "chat": 1,
    "turn": 2,
    "position": "0-25",
    "date": date(2017, 10, 24)
}

capsule_is_from_3 = {
    "utterance": "Selene is from Mexico",
    "subject": {"label": "selene", "type": "person"},
    "predicate": {"type": "be-from"},
    "object": {"label": "mexico", "type": "location"},
    "perspective": {"certainty": 1, "polarity": 1, "sentiment": 0},
    "author": "piek",
    "chat": 1,
    "turn": 3,
    "position": "0-25",
    "date": date(2017, 10, 24)
}

capsules = [capsule_is_from, capsule_is_from_2, capsule_is_from_3, capsule_knows]


def set_place(capsule, context):
    """
    Select a location randomly if not provided
    :return: place where scene takes place
    """
    if capsule.get('place', None) is not None:
        place = capsule['place']
    else:
        place = choice(places)

    context.location._label = place

    return context


def set_objects(capsule, context):
    """
    Create objects, related to the location if possible
    :param context: Context object containing information about the ongoing scene
    :param capsule: JSON
    :return: List of Object objects that are in the scene
    """
    if capsule.get('objects', None) is not None:
        objects = [Object(obj['type'], obj['confidence'], TEST_BOUNDS, TEST_IMG) for obj in capsule['objects']]
    else:
        # Office
        if context.location.label == 'Office':
            possible_objects = ['person', 'chair', 'laptop', 'bottle', 'plant']

        # Market
        elif context.location.label == 'Market':
            possible_objects = ['person', 'apple', 'banana', 'avocado', 'strawberry']

        # Playground
        elif context.location.label == 'Playground':
            possible_objects = ['person', 'teddy bear', 'cat', 'apple', 'banana']

        # Home
        elif context.location.label == 'Home':
            possible_objects = ['person', 'table', 'pills', 'chair']

        # Anywhere else
        else:
            possible_objects = unique_detections

        # Create and add objects
        num_objects = randint(0, len(possible_objects))
        objs = sample(possible_objects, num_objects)

        objects = []
        for ob in objs:
            confidence = uniform(0, 1)
            objects.append(Object(ob, confidence, TEST_BOUNDS, TEST_IMG))

    context.add_objects(objects)

    return context


def set_people(capsule, context):
    """
    Create people present in the scene
    :return: List of Face objects present in the scene
    """
    if capsule.get('people', None) is not None:
        faces = [Face(face['name'], face['confidence'], None, TEST_BOUNDS, TEST_IMG) for face in capsule['people']]
    else:
        # Add friends
        num_people = randint(0, len(friends))
        people = sample(friends, num_people)

        faces = set()
        for peep in people:
            confidence = uniform(0, 1)
            faces.add(Face(peep, confidence, None, TEST_BOUNDS, TEST_IMG))

        # Add strangers?
        if choice(binary_values):
            confidence = uniform(0, 1)
            faces.add(Face('Stranger', confidence, None, TEST_BOUNDS, TEST_IMG))

    context.add_people(faces)

    return context


def set_chat(capsule, context):
    """
    Create a Chat object, given a JSON representation and a Context object
    :param capsule: JSON
    :param context: Context object
    :return: Chat object
    """
    chat = Chat(capsule['author'], context)
    chat.id = capsule['chat']

    return chat


def set_utterance(capsule, chat):
    """
    Create an Utterance object, given a JSON representation and a Chat object
    :param capsule: JSON
    :param chat: Chat object
    :return: Utterance object
    """
    hyp = UtteranceHypothesis(capsule['utterance'], 0.99)

    utt = Utterance(chat, [hyp], False, capsule['turn'])
    utt._type = UtteranceType.STATEMENT
    utt.turn = capsule['turn']

    return utt


def set_triple(capsule, utt):
    """
    Create a Triple object given a JSON representation, and associate it to a given Utterance
    :param capsule: JSON
    :param utt: Utterance object
    :return:
    """
    builder = RdfBuilder()
    triple = builder.fill_triple(capsule['subject'], capsule['predicate'], capsule['object'])
    utt.triple = triple

    pers = set_perspective(capsule['perspective'])
    utt.perspective = pers


def set_perspective(persp):
    emotion = persp.get('emotion', Emotion.NEUTRAL)

    if type(emotion) != Emotion:
        emotion = Emotion[emotion.upper()]
    return Perspective(persp.get('certainty', 1), persp.get('polarity', 1), persp.get('sentiment', 0.0),
                       emotion=emotion)


def transform_capsule(capsule):
    """
    Take a JSON representation and create an Utterance object
    :param capsule: JSON
    :return: Utterance object
    """

    # Fake context
    context = Context(name, friends)

    # Set people
    context = set_people(capsule, context)

    # Set objects
    context = set_objects(capsule, context)

    # Set place
    context = set_place(capsule, context)

    # Set date
    context.set_datetime(capsule['date'])

    # Set chat
    chat = set_chat(capsule, context)

    # Set utterance
    utt = set_utterance(capsule, chat)

    # Set triple
    set_triple(capsule, utt)

    return utt
