# ruff: noqa: UP040

from enum import IntEnum
from typing import TypeAlias  # mypy is not supported PEP 695


class NumPlayer(IntEnum):
    FOUR = 4
    THREE = 3


class Round(IntEnum):
    EAST_1 = 1
    EAST_2 = 2
    EAST_3 = 3
    EAST_4 = 4
    SOUTH_1 = 5
    SOUTH_2 = 6
    SOUTH_3 = 7
    SOUTH_4 = 8


class _RecordRound(IntEnum):
    EAST_1 = 1
    EAST_2 = 2
    EAST_3 = 3
    EAST_4 = 4
    SOUTH_1 = 5
    SOUTH_2 = 6
    SOUTH_3 = 7
    SOUTH_4 = 8
    WEST_1 = 9
    WEST_2 = 10
    WEST_3 = 11
    WEST_4 = 12


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
