from datetime import date

from random import getrandbits

context_id, place_id = getrandbits(8), getrandbits(8)
chat_1 = [
    {
        "chat": 1,
        "turn": 1,
        "author": "piek",
        "utterance": "Lenka is from Serbia",
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "serbia",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "netherlands",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "mexico",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "suzana",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "croatia",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "selene-kolman",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "netherlands",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "serbia",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "goulash",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "romantic-movies",
            "type": "film-genre"
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
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "ice-cream",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "harry-potter",
            "type": "movie"
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
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "action-movies",
            "type": "film-genre"
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
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "balkenbrij",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "sailing",
            "type": "sport"
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
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "tacos",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "suzana",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "pizza",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "leolani",
            "type": "robot"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "france",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "type": "person",
            "label": "lenka"
        },
        "predicate": {
            "type": "mother-is"
        },
        "object": {
            "type": "person",
            "label": "ljubica"
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
        "position": "0-25",
        "subject": {
            "type": "person",
            "label": "lenka"
        },
        "predicate": {
            "type": "favorite-is"
        },
        "object": {
            "type": "dish",
            "label": "cake"
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
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "coco",
            "type": "movie"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "the_big-lebowski",
            "type": "movie"
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
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "2001_a_space-odyssey",
            "type": "movie"
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
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "horror-movies",
            "type": "film-genre"
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
        "position": "0-25",
        "subject": {
            "type": "person",
            "label": "bram"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "type": "film-genre",
            "label": "action-movies"
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
        "position": "0-25",
        "subject": {
            "type": "person",
            "label": "bram"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "type": "location",
            "label": "italy"
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
        "position": "0-21",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "goulash",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "baseball",
            "type": "sport"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "apple-pie",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "animated-movies",
            "type": "film-genre"
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
        "position": "0-25",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "acrobatics",
            "type": "sport"
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
        "position": "0-25",
        "subject": {
            "label": "leolani",
            "type": "robot"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "japan",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "type": "person",
            "label": "bram"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "type": "film-genre",
            "label": "romantic-movies"
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
        "position": "0-26",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "tacos",
            "type": "dish"
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
        "position": "0-12",
        "subject": {
            "label": "piek",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "tacos",
            "type": "dish"
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
        "position": "0-25",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "netherlands",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "piek",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "netherlands",
            "type": "location"
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
        "position": "0-25",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "soccer",
            "type": "sport"
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
        "position": "0-16",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "know"
        },
        "object": {
            "label": "lenka",
            "type": "person"
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
        "position": "0-16",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "know"
        },
        "object": {
            "label": "lenka",
            "type": "person"
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
        "position": "0-27",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "peru",
            "type": "location"
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
        "position": "0-22",
        "subject": {
            "label": "jaap",
            "type": "person"
        },
        "predicate": {
            "type": "have"
        },
        "object": {
            "label": "teapot",
            "type": "artifact"
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
        "position": "0-27",
        "subject": {
            "label": "lea",
            "type": "person"
        },
        "predicate": {
            "type": "favorite-color-is"
        },
        "object": {
            "label": "blue",
            "type": "adj.all"
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
        "position": "0-22",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "be"
        },
        "object": {
            "label": "tall",
            "type": "adj.all"
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
        "position": "0-26",
        "subject": {
            "label": "lea",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "swimming-and-biking",
            "type": "act"
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
        "position": "0-27",
        "subject": {
            "label": "lea",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "dusseldorf",
            "type": "location"
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
        "position": "0-19",
        "subject": {
            "label": "lea",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "celery",
            "type": "food"
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
        "position": "0-26",
        "subject": {
            "label": "thomas",
            "type": "person"
        },
        "predicate": {
            "type": "live-in"
        },
        "object": {
            "label": "berlin",
            "type": "location"
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
        "position": "0-16",
        "subject": {
            "label": "thomas",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "munich",
            "type": "location"
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
        "position": "0-21",
        "subject": {
            "label": "thomas",
            "type": "person"
        },
        "predicate": {
            "type": "study-in"
        },
        "object": {
            "label": "budapest",
            "type": "location"
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
        "position": "0-17",
        "subject": {
            "label": "thomas",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "asian-food",
            "type": "cuisine"
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
        "position": "0-23",
        "subject": {
            "label": "thomas",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "electronic-music",
            "type": "music"
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
        "position": "0-25",
        "subject": {
            "label": "lea",
            "type": "person"
        },
        "predicate": {
            "type": "hate"
        },
        "object": {
            "label": "cheese",
            "type": "food"
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
        "position": "0-20",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "dancing",
            "type": "act"
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
        "position": "0-18",
        "subject": {
            "label": "jaap",
            "type": "person"
        },
        "predicate": {
            "type": "have"
        },
        "object": {
            "label": "two-teapots",
            "type": "artifact"
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
        "position": "0-36",
        "subject": {
            "label": "jaap",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "chocolate-with-sea-salt",
            "type": "food"
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
        "position": "0-38",
        "subject": {
            "label": "lea",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "swimming-and-vikings",
            "type": "act"
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
        "position": "0-17",
        "subject": {
            "label": "tae",
            "type": "person"
        },
        "predicate": {
            "type": "speak"
        },
        "object": {
            "label": "german",
            "type": "adj.all"
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
        "position": "0-20",
        "subject": {
            "label": "tae",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "drinking-beer",
            "type": "interest"
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
        "position": "0-21",
        "subject": {
            "label": "tae",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "south-korea",
            "type": "location"
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
        "position": "0-13",
        "subject": {
            "label": "tae",
            "type": "person"
        },
        "predicate": {
            "type": "ride"
        },
        "object": {
            "label": "bike",
            "type": "transportation"
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
        "position": "0-11",
        "subject": {
            "label": "Tae",
            "type": "person"
        },
        "predicate": {
            "type": "hate"
        },
        "object": {
            "label": "rats",
            "type": "animal"
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
        "position": "0-19",
        "subject": {
            "label": "tae",
            "type": "person"
        },
        "predicate": {
            "type": "drink"
        },
        "object": {
            "label": "beer",
            "type": "interest"
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
        "position": "0-34",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "label": "romantic-movies",
            "type": "film-genre"
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
        "position": "0-19",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "peru",
            "type": "location"
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
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "",
            "label": "bram"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "type": "",
            "label": ""
        },
        "date": ""
    },
    {
        "chat": 12,
        "turn": 2,
        "author": "joey",
        "utterance": "Who is from Serbia?",
        "utterance_type": "question",
        "subject": {
            "label": "",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "serbia",
            "type": "location"
        }
    },
    {
        "chat": 12,
        "turn": 3,
        "author": "joey",
        "utterance": "Where is Lenka from?",
        "utterance_type": "question",
        "subject": {
            "label": "lenka",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "",
            "type": "location"
        }
    },
    {
        "chat": 12,
        "turn": 4,
        "author": "joey",
        "utterance_type": "question",
        "subject": {
            "label": "selene",
            "type": "person"
        },
        "predicate": {
            "type": "knows"
        },
        "object": {
            "label": "piek",
            "type": "person"
        }
    },
    {
        "chat": 12,
        "turn": 5,
        "author": "joey",
        "utterance": "Is Bram from the Netherlands?",
        "utterance_type": "question",
        "subject": {
            "label": "bram",
            "type": "person"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "label": "netherlands",
            "type": "location"
        }
    },
    {
        "chat": 12,
        "turn": 6,
        "author": "joey",
        "utterance": "Does Bram know Beyonce?",
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "person",
            "label": "bram"
        },
        "predicate": {
            "type": "knows"
        },
        "object": {
            "type": "",
            "label": "beyonce"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 7,
        "author": "joey",
        "utterance": "Do you know Bram?",
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "robot",
            "label": "leolani"
        },
        "predicate": {
            "type": "knows"
        },
        "object": {
            "type": "person",
            "label": "bram"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 8,
        "author": "joey",
        "utterance": "Does Selene know Piek?",
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "person",
            "label": "selene"
        },
        "predicate": {
            "type": "knows"
        },
        "object": {
            "type": "person",
            "label": "piek"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 9,
        "author": "joey",
        "utterance": "Where is Leolani from?",
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "robot",
            "label": "leolani"
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "type": "",
            "label": ""
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 10,
        "author": "joey",
        "utterance": "Who is from italy?",
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "",
            "label": ""
        },
        "predicate": {
            "type": "be-from"
        },
        "object": {
            "type": "",
            "label": "italy"
        },
        "date": date(2018, 3, 19)
    },
    {
        "chat": 12,
        "turn": 11,
        "author": "joey",
        "utterance": "what does Piek like?",
        "utterance_type": "question",
        "position": "",
        "subject": {
            "type": "",
            "label": "piek"
        },
        "predicate": {
            "type": "like"
        },
        "object": {
            "type": "",
            "label": ""
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
        "position": "0-15-0-15",
        "subject": {
            "label": "leolani",
            "type": "robot"
        },
        "predicate": {
            "type": "see"
        },
        "object": {
            "label": "apple",
            "type": "fruit"
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
