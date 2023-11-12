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
        self._provenance.casefold()

    def __repr__(self):
        return f'{self._provenance.__repr__()}'


class EntityNovelty(object):
    def __init__(self, subject, complement):
        # type: (dict, dict) -> None
        """
        Construct EntityNovelty Object
        Parameters
        ----------
        subject: dict
            Truth value for determining if this subject is something new, plus the entity involved
        complement: dict
            Truth value for determining if this complement is something new, plus the entity involved
        """
        self._subject = subject
        self._complement = complement

    @property
    def subject(self):
        # type: () -> dict
        return self._subject

    @property
    def complement(self):
        # type: () -> dict
        return self._complement

    @property
    def subject_novelty(self):
        # type: () -> dict
        return self._subject["value"]

    @property
    def complement_novelty(self):
        # type: () -> dict
        return self._complement["value"]

    def __repr__(self):
        subject = 'new' if self.subject_novelty else 'existing'
        complement = 'new' if self.complement_novelty else 'existing'
        return f'{subject} subject - {complement} object'
