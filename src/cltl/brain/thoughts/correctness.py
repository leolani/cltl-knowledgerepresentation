from cltl.brain.infrastructure.api import Provenance, Entity


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
        # type: () -> Entity
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
        # type: () -> Entity
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

