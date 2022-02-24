from datetime import date
from random import getrandbits

from cltl.combot.backend.api.discrete import UtteranceType

context_id, place_id = getrandbits(8), getrandbits(8)
chat_1 = [
    {
        "chat": 1,
        "turn": 1,
        "author": "piek",
        "utterance": "Lenka is from Serbia",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "serbia",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/serbia"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 10, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 1,
        "turn": 2,
        "author": "piek",
        "utterance": "Bram is from the Netherlands",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "netherlands",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/netherlands"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 10, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 1,
        "turn": 3,
        "author": "piek",
        "utterance": "Selene is from Mexico",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "mexico",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/mexico"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 10, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 1,
        "turn": 4,
        "author": "piek",
        "utterance": "Suzana is from Croatia",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "suzana",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/suzana"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "croatia",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/croatia"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 10, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 1,
        "turn": 5,
        "author": "piek",
        "utterance": "Selene Kolman is from the Netherlands",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene-2"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "netherlands",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/netherlands"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 10, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    }
]
context_id = getrandbits(8)
chat_2 = [
    {
        "chat": 2,
        "turn": 1,
        "author": "selene",
        "utterance": "I think Lenka is from Serbia",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "serbia",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/serbia"
        },
        "perspective": {
            "certainty": 0.5,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 2,
        "author": "selene",
        "utterance": "Bram likes goulash",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "goulash",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/goulash"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 3,
        "author": "selene",
        "utterance": "Bram likes romantic movies",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "romantic-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/romantic-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 4,
        "author": "selene",
        "utterance": "Lenka likes ice cream",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "ice-cream",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/ice-cream"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 5,
        "author": "selene",
        "utterance": "Lenka likes Harry Potter",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "harry-potter",
            "type": ["movie"],
            "uri": "http://cltl.nl/leolani/world/harry-potter"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 6,
        "author": "selene",
        "utterance": "Lenka likes action movies",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "action-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/action-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 7,
        "author": "selene",
        "utterance": "Piek likes balkenbrij",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "balkenbrij",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/balkenbrij"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 8,
        "author": "selene",
        "utterance": "Piek likes sailing",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "sailing",
            "type": ["sport"],
            "uri": "http://cltl.nl/leolani/world/sailing"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 9,
        "author": "selene",
        "utterance": "I like tacos",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "tacos",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/tacos"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 10,
        "author": "selene",
        "utterance": "Suzana likes pizza",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "suzana",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/suzana"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "pizza",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/pizza"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 2,
        "turn": 11,
        "author": "selene",
        "utterance": "Leolani is from France",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "leolani",
            "type": ["robot"],
            "uri": "http://cltl.nl/leolani/world/leolani"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "france",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/france"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 11, 17),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    }
]
context_id = getrandbits(8)
chat_3 = [
    {
        "chat": 3,
        "turn": 1,
        "author": "lenka",
        "utterance": "Lenka's mother is Ljubica ",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "mother-is",
            "uri": "http://cltl.nl/leolani/n2mu/mother-is"
        },
        "object": {
            "label": "ljubica",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/ljubica"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2018, 3, 20),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 3,
        "turn": 2,
        "author": "lenka",
        "utterance": "My favorite food is cake ",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "favorite-is",
            "uri": "http://cltl.nl/leolani/n2mu/favorite-is"
        },
        "object": {
            "label": "cake",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/cake"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2018, 3, 20),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 3,
        "turn": 3,
        "author": "lenka",
        "utterance": "Selene likes Coco",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "coco",
            "type": ["movie"],
            "uri": "http://cltl.nl/leolani/world/coco"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 20),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 3,
        "turn": 4,
        "author": "lenka",
        "utterance": "Bram likes The Big Lebowski",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "the_big-lebowski",
            "type": ["movie"],
            "uri": "http://cltl.nl/leolani/world/the_big-lebowski"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 20),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 3,
        "turn": 5,
        "author": "lenka",
        "utterance": "Piek likes 2001 A Space Odyssey",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "2001_a_space-odyssey",
            "type": ["movie"],
            "uri": "http://cltl.nl/leolani/world/2001_a_space-odyssey"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 20),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 3,
        "turn": 6,
        "author": "lenka",
        "utterance": "Piek likes horror movies",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "horror-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/horror-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 20),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_4 = [
    {
        "chat": 4,
        "turn": 1,
        "author": "bram",
        "utterance": "I like action movies ",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "action-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/action-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 2,
        "author": "bram",
        "utterance": "I am from Italy ",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "italy",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/italy"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 3,
        "author": "bram",
        "utterance": "I do not like goulash",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-21",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "goulash",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/goulash"
        },
        "perspective": {
            "certainty": 1,
            "polarity": -1,
            "sentiment": -1
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 4,
        "author": "bram",
        "utterance": "I like baseball",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "baseball",
            "type": ["sport"],
            "uri": "http://cltl.nl/leolani/world/baseball"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 5,
        "author": "bram",
        "utterance": "I like apple pie",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "apple-pie",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/apple-pie"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 6,
        "author": "bram",
        "utterance": "Selene likes animated movies",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "animated-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/animated-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 7,
        "author": "bram",
        "utterance": "Lenka likes acrobatics",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "acrobatics",
            "type": ["sport"],
            "uri": "http://cltl.nl/leolani/world/acrobatics"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 4,
        "turn": 8,
        "author": "bram",
        "utterance": "Leolani is from Japan",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "leolani",
            "type": ["robot"],
            "uri": "http://cltl.nl/leolani/world/leolani"
        },
        "predicate": {
            "label": "manufacture-in",
            "uri": "http://cltl.nl/leolani/n2mu/manufacture-in"
        },
        "object": {
            "label": "japan",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/japan"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2018, 3, 23),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_5 = [
    {
        "chat": 5,
        "turn": 1,
        "author": "piek",
        "utterance": "Bram likes romantic movies",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "romantic-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/romantic-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2018, 3, 25),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 5,
        "turn": 2,
        "author": "piek",
        "utterance": "Selene does not like tacos",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-26",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "tacos",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/tacos"
        },
        "perspective": {
            "certainty": 1,
            "polarity": -1,
            "sentiment": -1
        },
        "context_id": context_id,
        "date": date(2018, 3, 25),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 5,
        "turn": 3,
        "author": "piek",
        "utterance": "I hate tacos",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-12",
        "subject": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "tacos",
            "type": ["dish"],
            "uri": "http://cltl.nl/leolani/world/tacos"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": -1
        },
        "context_id": context_id,
        "date": date(2018, 3, 25),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_6 = [
    {
        "chat": 6,
        "turn": 1,
        "author": "suzana",
        "utterance": "Bram is not from the Netherlands",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "netherlands",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/netherlands"
        },
        "perspective": {
            "certainty": 1,
            "polarity": -1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2019, 5, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 6,
        "turn": 2,
        "author": "suzana",
        "utterance": "Piek is from the Netherlands",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "netherlands",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/netherlands"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2019, 5, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 6,
        "turn": 3,
        "author": "suzana",
        "utterance": "Selene likes soccer",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "soccer",
            "type": ["sport"],
            "uri": "http://cltl.nl/leolani/world/soccer"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2019, 5, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 6,
        "turn": 4,
        "author": "suzana",
        "utterance": "Bram knows Lenka",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-16",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "know",
            "uri": "http://cltl.nl/leolani/n2mu/know"
        },
        "object": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2019, 5, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 6,
        "turn": 5,
        "author": "suzana",
        "utterance": "Selene knows Lenka",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-16",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "know",
            "uri": "http://cltl.nl/leolani/n2mu/know"
        },
        "object": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2019, 5, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_7 = [
    {
        "chat": 7,
        "turn": 1,
        "author": "lenka",
        "utterance": "I think Selene is from Peru",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-27",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "peru",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/peru"
        },
        "perspective": {
            "certainty": 0.5,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 6, 9),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]

context_id = getrandbits(8)
chat_8 = [
    {
        "chat": 8,
        "turn": 1,
        "author": "lea",
        "utterance": "Jaap has three teapots",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-22",
        "subject": {
            "label": "jaap",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/jaap"
        },
        "predicate": {
            "label": "have",
            "uri": "http://cltl.nl/leolani/n2mu/have"
        },
        "object": {
            "label": "teapot",
            "type": ["artifact"],
            "uri": "http://cltl.nl/leolani/world/teapot"
        },
        "perspective": {
            "certainty": 0.75,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 8,
        "turn": 2,
        "author": "lea",
        "utterance": "My favourite colour is blue",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-27",
        "subject": {
            "label": "lea",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lea"
        },
        "predicate": {
            "label": "favorite-color-is",
            "uri": "http://cltl.nl/leolani/n2mu/favorite-color-is"
        },
        "object": {
            "label": "blue",
            "type": ["adj.all"],
            "uri": "http://cltl.nl/leolani/world/blue"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 8,
        "turn": 3,
        "author": "lea",
        "utterance": "I think Selene is tall",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-22",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "be",
            "uri": "http://cltl.nl/leolani/n2mu/be"
        },
        "object": {
            "label": "tall",
            "type": ["adj.all"],
            "uri": "http://cltl.nl/leolani/world/tall"
        },
        "perspective": {
            "certainty": 0.4,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 8,
        "turn": 4,
        "author": "lea",
        "utterance": "I like swimming and biking",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-26",
        "subject": {
            "label": "lea",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lea"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "swimming-and-biking",
            "type": ["act"],
            "uri": "http://cltl.nl/leolani/world/swimming-and-biking"
        },
        "perspective": {
            "certainty": 0.8,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 8,
        "turn": 5,
        "author": "lea",
        "utterance": "I'm from Dusseldorf",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-27",
        "subject": {
            "label": "lea",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lea"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "dusseldorf",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/dusseldorf"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 8,
        "turn": 6,
        "author": "lea",
        "utterance": "I don't like celery",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-19",
        "subject": {
            "label": "lea",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lea"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "celery",
            "type": ["food"],
            "uri": "http://cltl.nl/leolani/world/celery"
        },
        "perspective": {
            "certainty": 0.9,
            "polarity": -1,
            "sentiment": -1
        },
        "context_id": context_id,
        "date": date(2020, 9, 19),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_9 = [
    {
        "chat": 9,
        "turn": 1,
        "author": "thomas",
        "utterance": "I live in Berlin",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-26",
        "subject": {
            "label": "thomas",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/thomas"
        },
        "predicate": {
            "label": "live-in",
            "uri": "http://cltl.nl/leolani/n2mu/live-in"
        },
        "object": {
            "label": "berlin",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/berlin"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 21),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 9,
        "turn": 2,
        "author": "thomas",
        "utterance": "I am from Munich",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-16",
        "subject": {
            "label": "thomas",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/thomas"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "munich",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/munich"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 21),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 9,
        "turn": 3,
        "author": "thomas",
        "utterance": "I studied in Budapest",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-21",
        "subject": {
            "label": "thomas",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/thomas"
        },
        "predicate": {
            "label": "study-in",
            "uri": "http://cltl.nl/leolani/n2mu/study-in"
        },
        "object": {
            "label": "budapest",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/budapest"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 21),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 9,
        "turn": 4,
        "author": "thomas",
        "utterance": "I like Asian food",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-17",
        "subject": {
            "label": "thomas",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/thomas"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "asian-food",
            "type": ["cuisine"],
            "uri": "http://cltl.nl/leolani/world/asian-food"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 21),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 9,
        "turn": 5,
        "author": "thomas",
        "utterance": "I like electronic music",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-23",
        "subject": {
            "label": "thomas",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/thomas"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "electronic-music",
            "type": ["music"],
            "uri": "http://cltl.nl/leolani/world/electronic-music"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 21),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_10 = [
    {
        "chat": 10,
        "turn": 1,
        "author": "jaap",
        "utterance": "I think Lea hates cheese",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "subject": {
            "label": "lea",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lea"
        },
        "predicate": {
            "label": "hate",
            "uri": "http://cltl.nl/leolani/n2mu/hate"
        },
        "object": {
            "label": "cheese",
            "type": ["food"],
            "uri": "http://cltl.nl/leolani/world/cheese"
        },
        "perspective": {
            "certainty": 0.6,
            "polarity": 1,
            "sentiment": -1
        },
        "context_id": context_id,
        "date": date(2020, 9, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 10,
        "turn": 2,
        "author": "jaap",
        "utterance": "Selene likes dancing",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-20",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "dancing",
            "type": ["act"],
            "uri": "http://cltl.nl/leolani/world/dancing"
        },
        "perspective": {
            "certainty": 0.8,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 10,
        "turn": 3,
        "author": "jaap",
        "utterance": "I have two teapots",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-18",
        "subject": {
            "label": "jaap",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/jaap"
        },
        "predicate": {
            "label": "have",
            "uri": "http://cltl.nl/leolani/n2mu/have"
        },
        "object": {
            "label": "two-teapots",
            "type": ["artifact"],
            "uri": "http://cltl.nl/leolani/world/two-teapots"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 10,
        "turn": 4,
        "author": "jaap",
        "utterance": "I don't like chocolate with sea salt",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-36",
        "subject": {
            "label": "jaap",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/jaap"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "chocolate-with-sea-salt",
            "type": ["food"],
            "uri": "http://cltl.nl/leolani/world/chocolate-with-sea-salt"
        },
        "perspective": {
            "certainty": 1,
            "polarity": -1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 10,
        "turn": 5,
        "author": "jaap",
        "utterance": "I think Lea likes swimming and vikings",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-38",
        "subject": {
            "label": "lea",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lea"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "swimming-and-vikings",
            "type": ["act"],
            "uri": "http://cltl.nl/leolani/world/swimming-and-vikings"
        },
        "perspective": {
            "certainty": 0.2,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 10,
        "turn": 6,
        "author": "jaap",
        "utterance": "Tae speaks German",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-17",
        "subject": {
            "label": "tae",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/tae"
        },
        "predicate": {
            "label": "speak",
            "uri": "http://cltl.nl/leolani/n2mu/speak"
        },
        "object": {
            "label": "german",
            "type": ["adj.all"],
            "uri": "http://cltl.nl/leolani/world/german"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]
context_id = getrandbits(8)
chat_11 = [
    {
        "chat": 11,
        "turn": 1,
        "author": "tae",
        "utterance": "I like drinking beer",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-20",
        "subject": {
            "label": "tae",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/tae"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "drinking-beer",
            "type": ["interest"],
            "uri": "http://cltl.nl/leolani/world/drinking-beer"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 1
        },
        "context_id": context_id,
        "date": date(2020, 9, 29),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 11,
        "turn": 2,
        "author": "tae",
        "utterance": "I am from South Korea",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-21",
        "subject": {
            "label": "tae",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/tae"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "south-korea",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/south-korea"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 29),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 11,
        "turn": 3,
        "author": "tae",
        "utterance": "I ride a bike",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-13",
        "subject": {
            "label": "tae",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/tae"
        },
        "predicate": {
            "label": "ride",
            "uri": "http://cltl.nl/leolani/n2mu/ride"
        },
        "object": {
            "label": "bike",
            "type": ["transportation"],
            "uri": "http://cltl.nl/leolani/world/bike"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 29),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 11,
        "turn": 4,
        "author": "tae",
        "utterance": "I hate rats",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-11",
        "subject": {
            "label": "Tae",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/tae"
        },
        "predicate": {
            "label": "hate",
            "uri": "http://cltl.nl/leolani/n2mu/hate"
        },
        "object": {
            "label": "rats",
            "type": ["animal"],
            "uri": "http://cltl.nl/leolani/world/rats"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": -1
        },
        "context_id": context_id,
        "date": date(2020, 9, 29),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []},
    {
        "chat": 11,
        "turn": 5,
        "author": "tae",
        "utterance": "I do not drink beer",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-19",
        "subject": {
            "label": "tae",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/tae"
        },
        "predicate": {
            "label": "drink",
            "uri": "http://cltl.nl/leolani/n2mu/drink"
        },
        "object": {
            "label": "beer",
            "type": ["interest"],
            "uri": "http://cltl.nl/leolani/world/beer"
        },
        "perspective": {
            "certainty": 1,
            "polarity": -1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 9, 29),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []}
]

statements_old_team = chat_1 + chat_2 + chat_3 + chat_4 + chat_5 + chat_6 + chat_7
statements_new_team = chat_8 + chat_9 + chat_10 + chat_11
statements = statements_old_team + statements_new_team

context_id = getrandbits(8)
conflicting_statements = [
    {
        "chat": 12,
        "turn": 1,
        "author": "suzana",
        "utterance": "Bram does not like romantic movies",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-34",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "romantic-movies",
            "type": ["film-genre"],
            "uri": "http://cltl.nl/leolani/world/romantic-movies"
        },
        "perspective": {
            "certainty": 1,
            "polarity": -1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2020, 11, 3),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
    {
        "chat": 12,
        "turn": 2,
        "author": "suzana",
        "utterance": "Selene is from Peru",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-19",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "peru",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/peru"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "context_id": context_id,
        "date": date(2017, 10, 24),
        "place": "Piek's office",
        "place_id": place_id,
        "country": "Netherlands",
        "region": "North Holland",
        "city": "Amsterdam",
        "objects": [],
        "people": []
    },
]

questions = [
    {
        "chat": 12,
        "turn": 1,
        "author": "joey",
        "utterance": "Where is Bram from?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "bram",
            "type": [""],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "",
            "type": [""],
            "uri": ""
        },
        "date": ""
    },
    {
        "chat": 12,
        "turn": 2,
        "author": "joey",
        "utterance": "Who is from Serbia?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "",
            "type": ["person"],
            "uri": ""
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "serbia",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/serbia"
        },
        "date": ""
    },
    {
        "chat": 12,
        "turn": 3,
        "author": "joey",
        "utterance": "Where is Lenka from?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "lenka",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/lenka"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "",
            "type": ["location"],
            "uri": ""
        },
        "date": ""
    },
    {
        "chat": 12,
        "turn": 4,
        "author": "joey",
        "utterance": "Does Selene know Piek?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "know",
            "uri": "http://cltl.nl/leolani/n2mu/know"
        },
        "object": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "date": ""
    },
    {
        "chat": 12,
        "turn": 5,
        "author": "joey",
        "utterance": "Is Bram from the Netherlands?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "netherlands",
            "type": ["location"],
            "uri": "http://cltl.nl/leolani/world/netherlands"
        },
        "date": ""
    },
    {
        "chat": 12,
        "turn": 6,
        "author": "joey",
        "utterance": "Does Bram know Beyonce?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "predicate": {
            "label": "know",
            "uri": "http://cltl.nl/leolani/n2mu/know"
        },
        "object": {
            "label": "beyonce",
            "type": [""],
            "uri": "http://cltl.nl/leolani/world/beyonce"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 7,
        "author": "joey",
        "utterance": "Do you know Bram?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "leolani",
            "type": ["robot"],
            "uri": "http://cltl.nl/leolani/world/leolani"
        },
        "predicate": {
            "label": "know",
            "uri": "http://cltl.nl/leolani/n2mu/know"
        },
        "object": {
            "label": "bram",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/bram"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 8,
        "author": "joey",
        "utterance": "Does Selene know Piek?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "selene",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/selene"
        },
        "predicate": {
            "label": "know",
            "uri": "http://cltl.nl/leolani/n2mu/know"
        },
        "object": {
            "label": "piek",
            "type": ["person"],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 9,
        "author": "joey",
        "utterance": "Where is Leolani from?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "leolani",
            "type": ["robot"],
            "uri": "http://cltl.nl/leolani/world/leolani"
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "",
            "type": [""],
            "uri": ""
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 10,
        "author": "joey",
        "utterance": "Who is from italy?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "",
            "type": [""],
            "uri": ""
        },
        "predicate": {
            "label": "be-from",
            "uri": "http://cltl.nl/leolani/n2mu/be-from"
        },
        "object": {
            "label": "italy",
            "type": [""],
            "uri": "http://cltl.nl/leolani/world/italy"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 11,
        "author": "joey",
        "utterance": "what does Piek like?",
        "utterance_type": UtteranceType.QUESTION,
        "position": "",
        "subject": {
            "label": "piek",
            "type": [""],
            "uri": "http://cltl.nl/leolani/world/piek"
        },
        "predicate": {
            "label": "like",
            "uri": "http://cltl.nl/leolani/n2mu/like"
        },
        "object": {
            "label": "",
            "type": [""],
            "uri": ""
        },
        "date": date(2018, 3, 19)
    }
]

experiences = [
    {
        "chat": None,
        "turn": None,
        "author": "front_camera",
        "utterance": "",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-15-0-15",
        "subject": {
            "label": "leolani",
            "type": ["robot"],
            "uri": "http://cltl.nl/leolani/world/leolani"
        },
        "predicate": {
            "label": "see",
            "uri": "http://cltl.nl/leolani/n2mu/see"
        },
        "object": {
            "label": "apple",
            "type": ["fruit"],
            "uri": "http://cltl.nl/leolani/world/apple"
        },
        "perspective": {
            "certainty": 1,
            "polarity": 1,
            "sentiment": 0
        },
        "date": date(2018, 3, 19)
    }
]

visuals = ['laptop computer', 'pay-station', 'notebook', 'flowerpot', 'pot', 'tv', 'espresso maker', 'pay-phone',
           'desk', 'printer', 'tool kit', "carpenter's kit", 'chair', 'potted plant', "potter's wheel",
           'notebook computer', 'laptop']

sample_coco = ['Bag', 'backpack', 'handbag', 'suitcase', 'umbrella', 'tie', 'Animal', 'bird', 'cat', 'dog', 'horse',
               'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'Food', 'banana', 'apple', 'orange', 'carrot',
               'broccoli', 'cake', 'pizza', 'hot dog', 'donut', 'sandwich', 'Sports', 'tennis racket',
               'badminton racket', 'baseball bat', 'kite', 'snowboard', 'ball', 'basketball', 'Furniture', 'chair',
               'sofa', 'bed', 'toilet', 'couch', 'fridge', 'Office', 'keyboard', 'mouse', 'cellphone', 'tv', 'laptop',
               'Miscellaneous', 'Book', 'clock']

name = 'Leolani'
places = ['Forest', 'Playground', 'Monastery', 'House', 'University', 'Hotel', 'Office']
friends = ['Piek', 'Lenka', 'Bram', 'Suzana', 'Selene', 'Lea', 'Thomas', 'Jaap', 'Tae']
