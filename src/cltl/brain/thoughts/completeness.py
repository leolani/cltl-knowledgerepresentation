import random
from typing import List

from cltl.brain.infrastructure.api import Entity


class Gap(object):
    def __init__(self, known_entity, predicate, target_entity_type):
        # type: (Entity, Predicate, Entity) -> None
        """
        Construct Gap Object
        Parameters
        ----------
        predicate: Predicate
            Information about what can be known for the entity.
        entity: Entity Type
            Information about the type of things that can be known
        """
        self._known_entity = known_entity
        self._predicate = predicate
        self._target_entity_type = target_entity_type

    @property
    def known_entity(self):
        # type: () -> Entity
        return self._known_entity

    @property
    def predicate(self):
        # type: () -> Predicate
        return self._predicate

    @property
    def target_entity_type(self):
        # type: () -> Entity
        return self._target_entity_type

    @property
    def known_entity_name(self):
        # type: () -> str
        return self._known_entity.label

    @property
    def predicate_name(self):
        # type: () -> str
        return self._predicate.label

    @property
    def target_entity_range(self):
        # type: () -> List[str]
        return self._target_entity_type.types

    @property
    def target_entity_range_name(self):
        # type: () -> str
        return self._target_entity_type.types_names

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
        self._target_entity_type.casefold(format)
        self._predicate.casefold(format)

    def __repr__(self):
        return f'{self.known_entity_name} {self.predicate_name} {self.target_entity_range_name}'


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
