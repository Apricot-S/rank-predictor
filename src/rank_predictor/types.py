from enum import IntEnum, StrEnum


class NumPlayer(IntEnum):
    FOUR = 4
    THREE = 3


class GameLength(StrEnum):
    TONPU = "t"
    HANCHAN = "h"


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
    WEST_1 = 8
    WEST_2 = 9
    WEST_3 = 10
    WEST_4 = 11
