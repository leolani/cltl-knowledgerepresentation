from random import choice, sample, randint, uniform

import numpy as np
from datetime import date

from cltl.brain import RdfBuilder, Perspective
from cltl.brain_external import Context, Face, Object, Chat, Utterance, UtteranceHypothesis, UtteranceType, Emotion
from cltl.combot.infra.util import Bounds

TEST_IMG = np.zeros((128,))
TEST_BOUNDS = Bounds(0.0, 0.0, 0.5, 1.0)

name = 'Leolani'
places = ['Forest', 'Playground', 'Monastery', 'House', 'University', 'Hotel', 'Office']
friends = ['Piek', 'Lenka', 'Bram', 'Suzana', 'Selene', 'Lea', 'Thomas', 'Jaap', 'Tae']

signal = False
binary_values = [True]

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


def random_flags():
    """
    Determine if the scene will be modelled with objects, people and/or a known place
    :return:
    """
    objects_flag = choice(binary_values)
    people_flag = choice(binary_values)
    places_flag = choice(binary_values)

    return objects_flag, people_flag, places_flag


def fake_context(objects_flag=False, people_flag=False, places_flag=False):
    """
    Create a Context object representing a scene taking place in a location, with objects, people
    :param objects_flag: Whether there are objects in the scene
    :param people_flag: Whether there are people in the scene
    :param places_flag: Whether the in the scene is known or not
    :return: Context object
    """
    context = Context(name, friends)

    # Set place
    if places_flag:
        place = fake_place()
        context.location._label = place

    # Set objects
    if objects_flag:
        objects = fake_objects(context)
        context.add_objects(objects)

    # Set people
    if people_flag:
        faces = fake_people()
        context.add_people(faces)

    return context


def fake_place():
    """
    Select a location randomly
    :return: place where scene takes place
    """
    place = choice(places)

    return place


def fake_objects(context):
    """
    Create objects, related to the location if possible
    :param context: Context object containing information about the ongoing scene
    :return: List of Object objects that are in the scene
    """
    # Office
    if context.location.label == 'Office':
        if choice(binary_values):
            objects = [Object('person', 0.79, TEST_BOUNDS, TEST_IMG), Object('laptop', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('chair', 0.88, TEST_BOUNDS, TEST_IMG), Object('laptop', 0.51, TEST_BOUNDS, TEST_IMG),
                       Object('bottle', 0.88, TEST_BOUNDS, TEST_IMG)]
        else:
            objects = [Object('person', 0.79, TEST_BOUNDS, TEST_IMG), Object('plant', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('chair', 0.88, TEST_BOUNDS, TEST_IMG), Object('laptop', 0.51, TEST_BOUNDS, TEST_IMG)]

    # Market
    elif context.location.label == 'Market':
        if choice(binary_values):
            objects = [Object('apple', 0.79, TEST_BOUNDS, TEST_IMG), Object('banana', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('avocado', 0.51, TEST_BOUNDS, TEST_IMG), Object('banana', 0.88, TEST_BOUNDS, TEST_IMG)]
        else:
            objects = [Object('apple', 0.79, TEST_BOUNDS, TEST_IMG), Object('banana', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('avocado', 0.51, TEST_BOUNDS, TEST_IMG),
                       Object('strawberry', 0.88, TEST_BOUNDS, TEST_IMG)]

    # Playground
    elif context.location.label == 'Playground':
        if choice(binary_values):
            objects = [Object('person', 0.79, TEST_BOUNDS, TEST_IMG), Object('teddy bear', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('teddy bear', 0.88, TEST_BOUNDS, TEST_IMG), Object('cat', 0.51, TEST_BOUNDS, TEST_IMG)]
        else:
            objects = [Object('apple', 0.79, TEST_BOUNDS, TEST_IMG), Object('banana', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('cat', 0.51, TEST_BOUNDS, TEST_IMG), Object('banana', 0.88, TEST_BOUNDS, TEST_IMG)]

    # Home
    elif context.location.label == 'Home':
        objects = [Object('table', 0.89, TEST_BOUNDS, TEST_IMG), Object('pills', 0.88, TEST_BOUNDS, TEST_IMG)]

    # Anywhere else
    else:
        if choice(binary_values):
            objects = [Object('teddy bear', 0.79, TEST_BOUNDS, TEST_IMG), Object('dog', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('cat', 0.51, TEST_BOUNDS, TEST_IMG), Object('dog', 0.88, TEST_BOUNDS, TEST_IMG)]
        else:
            objects = [Object('apple', 0.79, TEST_BOUNDS, TEST_IMG), Object('banana', 0.88, TEST_BOUNDS, TEST_IMG),
                       Object('avocado', 0.51, TEST_BOUNDS, TEST_IMG),
                       Object('strawberry', 0.88, TEST_BOUNDS, TEST_IMG)]

    return objects


def fake_people():
    """
    Create people present in the scene
    :return: List of Face objects present in the scene
    """
    num_people = randint(0, len(friends))
    people = sample(friends, num_people)

    faces = set()
    for peep in people:
        confidence = uniform(0, 1)
        f = Face(peep, confidence, .90, TEST_BOUNDS, TEST_IMG)
        faces.add(f)

    # Add strangers?
    if choice(binary_values):
        confidence = uniform(0, 1)
        faces.add(Face('Stranger', confidence, .76, TEST_BOUNDS, TEST_IMG))

    return faces


def fake_chat(capsule, context):
    """
    Create a Chat object, given a JSON representation and a Context object
    :param capsule: JSON
    :param context: Context object
    :return: Chat object
    """
    chat = Chat(capsule['author'], context)
    chat.id = capsule['chat']

    return chat


def fake_utterance(capsule, chat):
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


def fake_triple(capsule, utt):
    """
    Create a Triple object given a JSON representation, and associate it to a given Utterance
    :param capsule: JSON
    :param utt: Utterance object
    :return:
    """
    builder = RdfBuilder()
    triple = builder.fill_triple(capsule['subject'], capsule['predicate'], capsule['object'])
    utt.triple = triple

    pers = pack_perspective(capsule['perspective'])
    utt.perspective = pers


def pack_perspective(persp):
    sentiment = persp.get('sentiment', 0.0)
    emotion = persp.get('emotion', Emotion.NEUTRAL)

    if type(emotion) != Emotion:
        emotion = Emotion[emotion.upper()]
    return Perspective(persp.get('certainty', 1), persp.get('polarity', 1), sentiment, emotion=emotion)


def transform_capsule(capsule, objects_flag=False, people_flag=False, places_flag=False):
    """
    Take a JSON representation and create an Utterance object
    :param capsule: JSON
    :param objects_flag: Whether there are objects in the scene
    :param people_flag: Whether there are people in the scene
    :param places_flag: Whether the in the scene is known or not
    :return: Utterance object
    """

    context = fake_context(objects_flag=objects_flag, people_flag=people_flag, places_flag=places_flag)
    context.set_datetime(capsule['date'])

    chat = fake_chat(capsule, context)
    utt = fake_utterance(capsule, chat)

    fake_triple(capsule, utt)

    return utt
