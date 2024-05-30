# ruff: noqa: UP040

from enum import IntEnum
from typing import TypeAlias  # mypy is not supported PEP 695


class NumPlayer(IntEnum):
    FOUR = 4
    THREE = 3


RankProbabilities4: TypeAlias = tuple[float, float, float, float]
RankProbabilities3: TypeAlias = tuple[float, float, float]
RankProbabilities: TypeAlias = RankProbabilities4 | RankProbabilities3


ProbabilityMatrix4: TypeAlias = tuple[
    RankProbabilities4,
    RankProbabilities4,
    RankProbabilities4,
    RankProbabilities4,
]
ProbabilityMatrix3: TypeAlias = tuple[
    RankProbabilities3,
    RankProbabilities3,
    RankProbabilities3,
]
ProbabilityMatrix: TypeAlias = ProbabilityMatrix4 | ProbabilityMatrix3
