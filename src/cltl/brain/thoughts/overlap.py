import random
from typing import List


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
        self._provenance.casefold()
        self._entity.casefold()

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
