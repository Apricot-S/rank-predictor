"""Provides types and functions for game settings."""

from enum import IntEnum, StrEnum


class NumPlayer(IntEnum):
    """Enum for the number of players.

    Attributes:
        FOUR: 4
        THREE: 3
    """

    FOUR = 4
    THREE = 3


class GameLength(StrEnum):
    """Enum for the length of a game.

    Attributes:
        TONPU: "t". Represents Tonpu (東風).
        HANCHAN: "h". Represents Hanchan (半荘).
    """

    TONPU = "t"
    HANCHAN = "h"


def get_game_length_name(game_length: GameLength) -> str:
    """Gets the full name of the game length.

    Args:
        game_length: Enum value representing the game length.

    Returns:
        Full name of the game length. It returns either "Tonpu" or
            "Hanchan", depending on the argument.
    """
    return "Tonpu" if game_length == GameLength.TONPU else "Hanchan"


class Round(IntEnum):
    """Enum for the rounds in a game.

    Attributes:
        EAST_1: 0. Represents East 1 (東1局).
        EAST_2: 1. Represents East 2 (東2局).
        EAST_3: 2. Represents East 3 (東3局).
        EAST_4: 3. Represents East 4 (東4局).
        SOUTH_1: 4. Represents South 1 (南1局).
        SOUTH_2: 5. Represents South 2 (南2局).
        SOUTH_3: 6. Represents South 3 (南3局).
        SOUTH_4: 7. Represents South 4 (南4局).
        WEST_1: 8. Represents West 1 (西1局).
        WEST_2: 9. Represents West 2 (西2局).
        WEST_3: 10. Represents West 3 (西3局).
        WEST_4: 11. Represents West 4 (西4局).
    """

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


class DataName(StrEnum):
    """Enum for the column names in annotated data.

    Attributes:
        ROUND: "round"
        NUM_COUNTER_STICK: "num_counter_stick"
        NUM_RIICHI_DEPOSIT: "num_riichi_deposit"
        SCORE: "score"
        RANK_CLASS: "rank_class"
    """

    ROUND = "round"
    NUM_COUNTER_STICK = "num_counter_stick"
    NUM_RIICHI_DEPOSIT = "num_riichi_deposit"
    SCORE = "score"
    RANK_CLASS = "rank_class"
