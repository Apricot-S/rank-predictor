# ruff: noqa: UP040

from enum import IntEnum, StrEnum
from typing import TypeAlias  # mypy is not supported PEP 695


class NumPlayer(IntEnum):
    FOUR = 4
    THREE = 3


def validate_num_player(num_player: NumPlayer) -> None:
    if num_player not in NumPlayer:
        msg = f"Unsupported number of players selected: {num_player}"
        raise ValueError(msg)


class GameLength(StrEnum):
    TONPU = "t"
    HANCHAN = "h"


def validate_game_length(game_length: GameLength) -> None:
    if game_length not in GameLength:
        msg = f"Unsupported game length selected: {game_length}"
        raise ValueError(msg)


def get_game_length_name(game_length: GameLength) -> str:
    return "Tonpu" if game_length == GameLength.TONPU else "Hanchan"


class DataName(StrEnum):
    ROUND = "round"
    NUM_COUNTER_STICK = "num_counter_stick"
    NUM_RIICHI_DEPOSIT = "num_riichi_deposit"
    SCORE = "score"
    RANK_CLASS = "rank_class"


class Round(IntEnum):
    EAST_1 = 0
    EAST_2 = 1
    EAST_3 = 2
    EAST_4 = 3
    SOUTH_1 = 4
    SOUTH_2 = 5
    SOUTH_3 = 6
    SOUTH_4 = 7


Scores4: TypeAlias = tuple[int, int, int, int]
Scores3: TypeAlias = tuple[int, int, int]
Scores: TypeAlias = Scores4 | Scores3

Ranks4: TypeAlias = tuple[int, int, int, int]
Ranks3: TypeAlias = tuple[int, int, int]
Ranks: TypeAlias = Ranks4 | Ranks3

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
