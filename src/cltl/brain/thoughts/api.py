from typing import List, Optional

from cltl.brain.thoughts.completeness import Gaps
from cltl.brain.thoughts.correctness import CardinalityConflict, NegationConflict
from cltl.brain.thoughts.novelty import StatementNovelty, EntityNovelty
from cltl.brain.thoughts.overlap import Overlaps


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
