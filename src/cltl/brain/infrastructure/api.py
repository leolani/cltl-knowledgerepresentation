import random
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

    def casefold(self, subject, complement, format='triple'):
        # type (str) -> ()
        """
        Format the labels to match triples or natural language
        Parameters
        ----------
        format

        Returns
        -------

        """

        subject_label = subject.label if subject is not None and subject.label not in ['', Literal('')] else (
            subject.types if subject is not None else '?')
        complement_label = complement.label if complement is not None and complement.label not in ['',
                                                                                                   Literal('')] else (
            complement.types if complement is not None else '?')

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
        self._predicate.casefold(self.subject, self.complement, format)

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
        # type: (Entity, date) -> None
        """
        Construct Provenance Object
        Parameters
        ----------
        author: Entity
            Person who said the mention
        date: date
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


class CardinalityConflict(object):
    def __init__(self, provenance, entity):
        # type: (Provenance, Entity) -> None
        """
        Construct CardinalityConflict Object
        Parameters
        ----------
        provenance: Provenance
            Information about who said the conflicting information and when
        entity: Entity
            Information about what the conflicting information is about
        """
        self._provenance = provenance
        self._complement = entity

    @property
    def provenance(self):
        # type: () -> Provenance
        return self._provenance

    @property
    def complement(self):
        # type: () -> Entity
        return self._complement

    @property
    def author(self):
        # type: () -> str
        return self._provenance.author

    @property
    def date(self):
        # type: () -> date
        return self._provenance.date

    @property
    def complement_name(self):
        # type: () -> str
        return self._complement.label

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
        self._provenance.casefold(format)
        self._complement.casefold(format)

    def __repr__(self):
        return f'{self._provenance.__repr__()} about {self.complement_name}'


class NegationConflict(object):
    def __init__(self, provenance, polarity_value):
        # type: (Provenance, polarity_value) -> None
        """
        Construct CardinalityConflict Object
        Parameters
        ----------
        provenance: Provenance
            Information about who said the conflicting information and when
        polarity_value: str
            Information about polarity of the statement
        """
        self._provenance = provenance
        self._polarity_value = polarity_value

    @property
    def provenance(self):
        # type: () -> Provenance
        return self._provenance

    @property
    def polarity_value(self):
        # type: () -> str
        return self._polarity_value

    @property
    def author(self):
        # type: () -> str
        return self._provenance.author

    @property
    def date(self):
        # type: () -> date
        return self._provenance.date

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
        self._provenance.casefold(format)

        # TODO: Cannot Casefold String, uncommented for now?
        # self._polarity_value.casefold(format)

    def __repr__(self):
        return f'{self._provenance.__repr__()} about {self.polarity_value}'


# TODO revise overlap with provenance
class StatementNovelty(object):
    def __init__(self, provenance):
        # type: (Provenance) -> None
        """
        Construct StatementNovelty Object
        Parameters
        ----------
        provenance: Provenance
            Information about who said the acquired information and when
        """
        self._provenance = provenance

    @property
    def provenance(self):
        # type: () -> Provenance
        return self._provenance

    @property
    def author(self):
        # type: () -> str
        return self._provenance.author

    @property
    def date(self):
        # type: () -> date
        return self._provenance.date

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
        self._provenance.casefold(format)

    def __repr__(self):
        return f'{self._provenance.__repr__()}'


class EntityNovelty(object):
    def __init__(self, existence_subject, existence_complement):
        # type: (bool, bool) -> None
        """
        Construct EntityNovelty Object
        Parameters
        ----------
        existence_subject: bool
            Truth value for determining if this subject is something new
        existence_complement: bool
            Truth value for determining if this complement is something new
        """
        self._subject = not existence_subject
        self._complement = not existence_complement

    @property
    def subject(self):
        # type: () -> bool
        return self._subject

    @property
    def complement(self):
        # type: () -> bool
        return self._complement

    def __repr__(self):
        subject = 'new' if self.subject else 'existing'
        complement = 'new' if self.complement else 'existing'
        return f'{subject} subject - {complement} object'


class Gap(object):
    def __init__(self, known_entity, predicate, entity):
        # type: (Entity, Predicate, Entity) -> None
        """
        Construct Gap Object
        Parameters
        ----------
        predicate: Predicate
            Information about what can be known for the entity
        entity: Entity
            Information about the type of things that can be known
        """
        self._known_entity = known_entity
        self._predicate = predicate
        self._entity = entity

    @property
    def known_entity(self):
        # type: () -> Entity
        return self._known_entity

    @property
    def predicate(self):
        # type: () -> Predicate
        return self._predicate

    @property
    def entity(self):
        # type: () -> Entity
        return self._entity

    @property
    def known_entity_name(self):
        # type: () -> str
        return self._known_entity.label

    @property
    def predicate_name(self):
        # type: () -> str
        return self._predicate.label

    @property
    def entity_range(self):
        # type: () -> List[str]
        return self._entity.types

    @property
    def entity_range_name(self):
        # type: () -> str
        return self._entity.types_names

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
        self._known_entity.casefold(format)
        self._entity.casefold(format)
        self._predicate.casefold(self.entity, None, format)

    def __repr__(self):
        return f'{self.known_entity_name} {self.predicate_name} {self.entity_range_name}'


class Gaps(object):
    def __init__(self, subject_gaps, complement_gaps):
        # type: (List[Gap], List[Gap]) -> None
        """
        Construct Gap Object
        Parameters
        ----------
        subject_gaps: List[Gap]
            List of gaps with potential things to learn about the original subject
        complement_gaps: List[Gap]
            List of gaps with potential things to learn about the original complement
        """
        self._subject = subject_gaps
        self._complement = complement_gaps

    @property
    def subject(self):
        # type: () -> List[Gap]
        return self._subject

    @property
    def complement(self):
        # type: () -> List[Gap]
        return self._complement

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
        for g in self._subject:
            g.casefold(format)
        for g in self._complement:
            g.casefold(format)

    def __repr__(self):
        s = random.choice(self._subject) if self._subject else ''
        o = random.choice(self._complement) if self._complement else ''
        return f'{len(self._subject)} gaps as subject: e.g. {s.__repr__()} - ' \
               f'{len(self._complement)} gaps as object: e.g. {o.__repr__()}'

    def __len__(self):
        return len(self._subject) + len(self._complement)


class Overlap(object):
    def __init__(self, provenance, entity):
        # type: (Provenance, Entity) -> None
        """
        Construct Overlap Object
        Parameters
        ----------
        provenance
        entity
        """
        self._provenance = provenance
        self._entity = entity

    @property
    def provenance(self):
        # type: () -> Provenance
        return self._provenance

    @property
    def entity(self):
        # type: () -> Entity
        return self._entity

    @property
    def author(self):
        # type: () -> str
        return self._provenance.author

    @property
    def date(self):
        # type: () -> date
        return self._provenance.date

    @property
    def entity_name(self):
        # type: () -> str
        return self._entity.label

    @property
    def entity_types(self):
        # type: () -> List[str]
        return self._entity.types

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
        self._provenance.casefold(format)
        self._entity.casefold(format)

    def __repr__(self):
        return f'{self._provenance.__repr__()} about {self.entity_name}'


class Overlaps(object):
    def __init__(self, subject_overlaps, complement_overlaps):
        # type: (List[Overlap], List[Overlap]) -> None
        """
        Construct Overlap Object
        Parameters
        ----------
        subject_overlaps: List[Overlap]
            List of overlaps shared with original subject
        complement_overlaps: List[Overlap]
            List of overlaps shared with original complement
        """
        self._subject = subject_overlaps
        self._complement = complement_overlaps

    @property
    def subject(self):
        # type: () -> List[Overlap]
        return self._subject

    @property
    def complement(self):
        # type: () -> List[Overlap]
        return self._complement

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
        for g in self._subject:
            g.casefold(format)
        for g in self._complement:
            g.casefold(format)

    def __repr__(self):
        s = random.choice(self._subject) if self._subject else ''
        o = random.choice(self._complement) if self._complement else ''
        return f'{len(self._subject)} subject overlaps: e.g. {s.__repr__()} - ' \
               f'{len(self._complement)} object overlaps: e.g. {o.__repr__()}'

    def __len__(self):
        return len(self._subject) + len(self._complement)


class Thoughts(object):
    def __init__(self, statement_novelty, entity_novelty, negation_conflicts, complement_conflict,
                 subject_gaps, complement_gaps, overlaps, trust):
        # type: (Optional[List[StatementNovelty]], Optional[EntityNovelty], Optional[List[NegationConflict]], Optional[List[CardinalityConflict]], Optional[Gaps], Optional[Gaps], Optional[Overlaps], Optional[float]) -> None
        """
        Construct Thoughts Object
        Parameters
        ----------
        statement_novelty: List[StatementNovelty]
            Information if the statement is novel
        entity_novelty: EntityNovelty
            Information if the entities involved are novel
        negation_conflicts: Optional[List[NegationConflict]]
            Information regarding conflicts of opposing statements heard
        complement_conflict: List[CardinalityConflict]
            Information regarding conflicts by violating one to one predicates
        subject_gaps: Gaps
            Information about what can be learned of the subject
        complement_gaps: Gaps
            Information about what can be learned of the complement
        overlaps: Overlaps
            Information regarding overlaps of this statement with things heard so far
        trust: float
            Level of trust on this actor
            :rtype: object
        """

        self._statement_novelty = statement_novelty
        self._entity_novelty = entity_novelty
        self._negation_conflicts = negation_conflicts
        self._complement_conflict = complement_conflict
        self._subject_gaps = subject_gaps
        self._complement_gaps = complement_gaps
        self._overlaps = overlaps
        self._trust = trust

    def complement_conflicts(self):
        # type: () -> List[CardinalityConflict]
        return self._complement_conflict

    def negation_conflicts(self):
        # type: () -> List[NegationConflict]
        return self._negation_conflicts

    def statement_novelties(self):
        # type: () -> List[StatementNovelty]
        return self._statement_novelty

    def entity_novelty(self):
        # type: () -> EntityNovelty
        return self._entity_novelty

    def complement_gaps(self):
        # type: () -> Gaps
        return self._complement_gaps

    def subject_gaps(self):
        # type: () -> Gaps
        return self._subject_gaps

    def overlaps(self):
        # type: () -> Overlaps
        return self._overlaps

    def trust(self):
        # type: () -> float
        return self._trust

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
        for n in self._statement_novelty:
            n.casefold(format)
        for c in self._negation_conflicts:
            c.casefold(format)
        for c in self._complement_conflict:
            c.casefold(format)
        if self._subject_gaps:
            self._subject_gaps.casefold(format)
        if self._complement_gaps:
            self._complement_gaps.casefold(format)
        if self._overlaps:
            self._overlaps.casefold(format)

    def __repr__(self):
        representation = {'statement_novelty': self._statement_novelty, 'entity_novelty': self._entity_novelty,
                          'negation_conflicts': self._negation_conflicts,
                          'complement_conflict': self._complement_conflict,
                          'subject_gaps': self._subject_gaps, 'complement_gaps': self._complement_gaps,
                          'overlaps': self._overlaps}

        return f'{representation}'
