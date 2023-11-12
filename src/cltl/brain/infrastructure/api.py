from datetime import date, datetime
from typing import List, Optional

from cltl.commons.casefolding import casefold_text
from cltl.commons.discrete import Certainty, Polarity, Sentiment, Emotion, Time
from cltl.commons.triple_helpers import filtered_types_names
from rdflib import Literal

from cltl.brain.utils.helper_functions import hash_claim_id, is_proper_noun


class RDFBase(object):
    def __init__(self, id, label, offset=None, confidence=0.0):
        # type: (str, str, Optional[slice], float) -> None
        """
        Construct RDFBase Object
        Parameters
        ----------
        id: str
            URI of RDFBase
        label: str
            Label of RDFBase
        offset: Optional[slice]
            Indeces of substring where this RDFBase was mentioned
        confidence: float
            Confidence value that this RDFBase was mentioned
        """

        self._id = id
        self._label = label
        self._offset = offset
        self._confidence = confidence

    @property
    def id(self):
        # type: () -> str
        return self._id

    @property
    def label(self):
        # type: () -> str
        return self._label

    @property
    def offset(self):
        # type: () -> Optional[slice]
        return self._offset

    @property
    def confidence(self):
        # type: () -> float
        return self._confidence

    def casefold(self, format='triple'):
        # type (str) -> ()
        """
        Format the labels to match triples or natural language
        Parameters
        ----------
        format

        Returns
        -------

        """
        if format == 'triple':
            # Label
            self._label = Literal(casefold_text(self.label, format=format))

        elif format == 'natural':
            # Label
            self._label = casefold_text(self.label, format=format)

    def __repr__(self):
        return f'{self.label}'


class Entity(RDFBase):
    def __init__(self, id, label, types, offset=None, confidence=0.0):
        # type: (str, str, List[str], Optional[slice], float) -> None
        """
        Construct Entity Object
        Parameters
        ----------
        id: str
            URI of entity
        label: str
            Label of entity
        types: List[str]
            List of types for this entity
        offset: Optional[slice]
            Indeces of substring where this entity was mentioned
        confidence: float
            Confidence value that this entity was mentioned
        """
        super(Entity, self).__init__(id, label, offset, confidence)

        self._types = [t for t in types if t != '' and t is not None]

    @property
    def types(self):
        # type: () -> List[str]
        return self._types

    @property
    def types_names(self):
        # type: () -> str
        return filtered_types_names(self._types)

    def add_types(self, types):
        # type: (List[str]) -> ()
        fixed_types = [t for t in types if t != '' and t is not None]
        self._types.extend(fixed_types)

    def casefold(self, format='triple'):
        # type (str) -> ()
        """
        Format the labels to match triples or natural language
        Parameters
        ----------
        format

        Returns
        -------

        """
        if format == 'triple':
            # Label
            self._label = Literal(casefold_text(self.label, format=format))
            # Types
            self._types = [casefold_text(t, format=format) for t in self.types]

        elif format == 'natural':
            # Label
            self._label = casefold_text(self.label, format=format)
            self._label = self._label.capitalize() if is_proper_noun(self.types) else self._label
            # Types
            self._types = [t.lower().replace("_", " ") for t in self.types]


class Predicate(RDFBase):
    def __init__(self, id, label, offset=None, confidence=0.0, cardinality=1):
        # type: (str, str, Optional[slice], float, int) -> None
        """
        Construct Predicate Object
        Parameters
        ----------
        id: str
            URI of predicate
        label: str
            Label of predicate
        offset: Optional[slice]
            Indeces of substring where this predicate was mentioned
        confidence: float
            Confidence value that this predicate was mentioned
        cardinality: int
            Represents relation of predicate (Range cardinality)
        """
        super(Predicate, self).__init__(id, label, offset, confidence)

        self._cardinality = cardinality

    @property
    def cardinality(self):
        # type: () -> int
        return self._cardinality

    def casefold(self, format='triple'):
        # type (str) -> ()
        """
        Format the labels to match triples or natural language
        Parameters
        ----------
        format

        Returns
        -------

        """

        # subject_label = subject.label if subject is not None and subject.label not in ['', Literal('')] \
        #     else (subject.types if subject is not None else '?')
        # complement_label = complement.label if complement is not None and complement.label not in ['', Literal('')] \
        #     else (complement.types if complement is not None else '?')

        if format == 'triple':
            # Label
            self._label = Literal(casefold_text(self.label, format=format))

        elif format == 'natural':
            # Label
            self._label = casefold_text(self.label, format=format)


class Triple(object):
    def __init__(self, subject, predicate, complement):
        # type: (Entity, Predicate, Entity) -> None
        """
        Construct Triple Object
        Parameters
        ----------
        subject: Entity
            Instance that is the subject of the information just received
        predicate: Predicate
            Predicate of the information just received
        complement: Entity
            Instance that is the complement of the information just received
        """

        self._subject = subject
        self._predicate = predicate
        self._complement = complement

    @property
    def subject(self):
        # type: () -> Entity
        return self._subject

    @subject.setter
    def subject(self, new_subject):
        # type: (Entity) -> None
        self._subject = new_subject

    @property
    def predicate(self):
        # type: () -> Predicate
        return self._predicate

    @predicate.setter
    def predicate(self, new_predicate):
        # type: (Predicate) -> None
        self._predicate = new_predicate

    @property
    def complement(self):
        # type: () -> Entity
        return self._complement

    @complement.setter
    def complement(self, new_complement):
        # type: (Entity) -> None
        self._complement = new_complement

    @property
    def subject_name(self):
        # type: () -> str
        return self._subject.label if self._subject is not None else None

    @property
    def predicate_name(self):
        # type: () -> str
        return self._predicate.label if self._predicate is not None else None

    @property
    def complement_name(self):
        # type: () -> str
        return self._complement.label if self._complement is not None else None

    @property
    def subject_types(self):
        # type: () -> str
        return self._subject.types_names if self._subject is not None else None

    @property
    def complement_types(self):
        # type: () -> str
        return self._complement.types_names if self._complement is not None else None

    def casefold(self, format='triple'):
        # type (str) -> ()
        """
        Format the labels to match triples or natural language
        Parameters
        ----------
        format

        Returns
        -------

        """
        self._subject.casefold(format)
        self._complement.casefold(format)
        self._predicate.casefold(format)

    def __iter__(self):
        return iter([('subject', self.subject), ('predicate', self.predicate), ('complement', self.complement)])

    def __repr__(self):
        hashed_triple = hash_claim_id([self.subject_name
                                       if self.subject_name is not None
                                          and self.subject_name not in ['', Literal('')] else '?',
                                       self.predicate_name
                                       if self.predicate_name is not None
                                          and self.predicate_name not in ['', Literal('')] else '?',
                                       self.complement_name
                                       if self.complement_name is not None
                                          and self.complement_name not in ['', Literal('')] else '?'])
        hashed_types = hash_claim_id([self.subject_types if self.subject_types is not None else '?',
                                      '->',
                                      self.complement_types if self.complement_types is not None else '?'])
        return f'{hashed_triple} [{hashed_types}])'


class Perspective(object):
    def __init__(self, certainty, polarity, sentiment, time=None, emotion=None):
        # type: (Certainty, Polarity, Sentiment, Time, Emotion) -> None
        """
        Construct Perspective Object
        Parameters
        ----------
        certainty: Certainty
            Enumerator representing certainty
        polarity: Polarity
            Enumerator representing polarity. Main flag to signal negation
        sentiment: float
            Enumerator representing sentiment
            positive sentiments.
        time: Time
            Enumerator representing time. This is extracted from the tense
        emotion: Emotion
            Enumerator representing one of the 6 universal emotions.
        """
        self._certainty = certainty
        self._polarity = polarity
        self._sentiment = sentiment
        self._time = time
        self._emotion = emotion

    @property
    def certainty(self):
        # type: () -> Certainty
        return self._certainty

    @certainty.setter
    def certainty(self, new_certainty):
        # type: (Certainty) -> ()
        self._certainty = new_certainty

    @property
    def polarity(self):
        # type: () -> Polarity
        return self._polarity

    @polarity.setter
    def polarity(self, new_polarity):
        # type: (Polarity) -> ()
        self._polarity = new_polarity

    @property
    def sentiment(self):
        # type: () -> Sentiment
        return self._sentiment

    @sentiment.setter
    def sentiment(self, new_sentiment):
        # type: (Sentiment) -> ()
        self._sentiment = new_sentiment

    @property
    def time(self):
        # type: () -> Optional[Time]
        return self._time

    @time.setter
    def time(self, new_time):
        # type: (Time) -> ()
        self._time = new_time

    @property
    def emotion(self):
        # type: () -> Optional[Emotion]
        return self._emotion

    @emotion.setter
    def emotion(self, new_emotion):
        # type: (Emotion) -> ()
        self._emotion = new_emotion


class Provenance(object):
    def __init__(self, author, date):
        # type: (Entity, str) -> None
        """
        Construct Provenance Object
        Parameters
        ----------
        author: Entity
            Person who said the mention
        date: str
            Date when the mention was said
        """

        self._author = author
        self._date = datetime.strptime(date, '%Y-%m-%d').date()

    @property
    def author(self):
        # type: () -> Entity
        return self._author

    @property
    def author_name(self):
        # type: () -> str
        return self._author.label if self._author is not None else None

    @property
    def author_types(self):
        # type: () -> str
        return self._author.types_names if self._author is not None else None

    @property
    def date(self):
        # type: () -> date
        return self._date

    def casefold(self, format='triple'):
        # type (str) -> ()
        """
        Format the labels to match triples or natural language
        Parameters
        ----------
        format

        Returns
        -------

        """
        self._author.casefold(format)

    def __repr__(self):
        return f'{self.author} on {self.date.strftime("%B,%Y")}'
