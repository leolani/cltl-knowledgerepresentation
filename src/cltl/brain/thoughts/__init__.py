"""
The Pepper Brain.thoughts Package contains infrastructure to create thoughts related to incoming information
"""

from cltl.brain.thoughts.completeness import Gaps, Gap
from cltl.brain.thoughts.correctness import CardinalityConflict, NegationConflict
from cltl.brain.thoughts.novelty import StatementNovelty, EntityNovelty
from cltl.brain.thoughts.overlap import Overlaps, Overlap
from cltl.brain.thoughts.thought_generator import ThoughtGenerator
