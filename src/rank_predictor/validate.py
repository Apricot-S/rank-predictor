"""Provides functionality to validate data."""

from collections.abc import Sequence
from typing import Final, assert_never

import polars as pl

from rank_predictor.rank import RANK_CLASS_3, RANK_CLASS_4
from rank_predictor.types import (
    DataName,
    GameLength,
    NumPlayer,
    Round,
    get_game_length_name,
)

TOTAL_SCORE_4: Final[int] = 1_000
TOTAL_SCORE_3: Final[int] = 1_050


def validate_annotated_data(
    num_player: NumPlayer,
    game_length: GameLength,
    annotated_data: pl.DataFrame,
) -> None:
    """Validates annotated data.

    Check if all annotated data are valid values.

    Args:
        num_player: The number of player in the annotated data.
        game_length: The length of the game in the annotated data.
        annotated_data: A DataFrame containing annotated data.

    Raises:
        ValueError: If the annotated data does not contain required
            values or contains invalid values.
    """
    required_columns = [
        DataName.ROUND,
        DataName.NUM_COUNTER_STICK,
        DataName.NUM_RIICHI_DEPOSIT,
        *[f"{DataName.SCORE}_{i}" for i in range(num_player)],
        DataName.RANK_CLASS,
    ]

    columns = annotated_data.columns
    missing_columns = [r for r in required_columns if r not in columns]
    if missing_columns:
        msg = f"The data is missing columns: {missing_columns}"
        raise ValueError(msg)

    if (num_player == NumPlayer.THREE) and (f"{DataName.SCORE}_3" in columns):
        msg = f"The data for 3-player contains `{DataName.SCORE}_3`."
        raise ValueError(msg)

    for name in required_columns:
        column_data = annotated_data.select(pl.col(name)).to_series()
        if not column_data.dtype.is_integer():
            msg = f"`{name}` column datatype is not an integer."
            raise ValueError(msg)
        if column_data.is_null().any():
            msg = f"`{name}` column contains null values."
            raise ValueError(msg)
        if (column_data < 0).any():
            msg = f"`{name}` column contains negative values."
            raise ValueError(msg)

    invalid_round = (
        Round.WEST_1 if game_length == GameLength.TONPU else (Round.WEST_4 + 1)
    )
    contains_invalid_round = not annotated_data.filter(
        pl.col(DataName.ROUND) >= invalid_round,
    ).is_empty()
    if contains_invalid_round:
        round_name = "West" if game_length == GameLength.TONPU else "North"
        msg = (
            f"The data for {get_game_length_name(game_length)} contains rounds"
            f" after {round_name}-1."
        )
        raise ValueError(msg)

    expected_total_score = (
        TOTAL_SCORE_4 if num_player == NumPlayer.FOUR else TOTAL_SCORE_3
    )
    contains_invalid_score = (
        (
            annotated_data.select(
                *[pl.col(f"{DataName.SCORE}_{i}") for i in range(num_player)],
                pl.col(DataName.NUM_RIICHI_DEPOSIT) * 10,
            ).sum_horizontal()
        )
        != expected_total_score
    ).any()
    if contains_invalid_score:
        msg = (
            "The data contains invalid scores. The sum of scores should be"
            f" {expected_total_score}."
        )
        raise ValueError(msg)

    num_rank_class = (
        len(RANK_CLASS_4)
        if num_player == NumPlayer.FOUR
        else len(RANK_CLASS_3)
    )
    contains_invalid_rank_class = not annotated_data.filter(
        pl.col(DataName.RANK_CLASS) >= num_rank_class,
    ).is_empty()
    if contains_invalid_rank_class:
        msg = f"`{DataName.RANK_CLASS}` column contains invalid values."
        raise ValueError(msg)

    expected_rank_classes = pl.LazyFrame(
        {DataName.RANK_CLASS: list(range(num_rank_class))},
    )
    unique_rank_classes_from_data = (
        annotated_data.lazy().select(pl.col(DataName.RANK_CLASS)).unique()
    )
    missing_rank_class = expected_rank_classes.join(
        unique_rank_classes_from_data,
        on=DataName.RANK_CLASS,
        how="anti",
    ).collect()
    if not missing_rank_class.is_empty():
        msg = (
            f"`{DataName.RANK_CLASS}` column does not contain"
            f" {missing_rank_class.to_series().to_list()}."
        )
        raise ValueError(msg)


def validate_score_4(score: int) -> None:
    """Validates a score for 4-player mahjong.

    Checks if the score for 4-player mahjong is within the valid range.
    The score must be a non-negative integer and must not exceed the
    total score of the 4 players.
    Omit the last two digits of the score.

    Args:
        score: The player's score for 4-player mahjong.

    Raises:
        ValueError: If the score is less than 0 or greater than the
            total score of the 4 players.
    """
    if score < 0 or score > TOTAL_SCORE_4:
        msg = f"The score for 4-player is incorrect.: {score}"
        raise ValueError(msg)


def validate_score_3(score: int) -> None:
    """Validates a score for 3-player mahjong.

    Checks if the score for 3-player mahjong is within the valid range.
    The score must be a non-negative integer and must not exceed the
    total score of the 3 players.
    Omit the last two digits of the score.

    Args:
        score: The player's score for 3-player mahjong.

    Raises:
        ValueError: If the score is less than 0 or greater than the
            total score of the 3 players.
    """
    if score < 0 or score > TOTAL_SCORE_3:
        msg = f"The score for 3-player is incorrect.: {score}"
        raise ValueError(msg)


def validate_score(score: int, num_player: NumPlayer) -> None:
    """Validates a score.

    Checks if the score is within the valid range.
    The score must be a non-negative integer and must not exceed the
    total score of the specified number of players.
    Omit the last two digits of the score.

    Args:
        score: The player's score.
        num_player: The number of players.

    Raises:
        ValueError: If the score is less than 0 or greater than the
            total score of the specified number of players.
    """
    match num_player:
        case NumPlayer.FOUR:
            validate_score_4(score)
        case NumPlayer.THREE:
            validate_score_3(score)
        case unreachable:
            assert_never(unreachable)


def validate_total_score_4(total_score: int) -> None:
    """Validates a total score for 4-player mahjong.

    Checks if the total score matches the total score required by the
    rule of 4-player mahjong.
    Omit the last two digits of the score.

    Args:
        total_score: The total score for 4-player mahjong.

    Raises:
        ValueError: If the total score does not match the total score
            required by the rules.
    """
    if total_score != TOTAL_SCORE_4:
        msg = f"The total score of 4-player is incorrect.: {total_score}"
        raise ValueError(msg)


def validate_total_score_3(total_score: int) -> None:
    """Validates a total score for 3-player mahjong.

    Checks if the total score matches the total score required by the
    rule of 3-player mahjong.
    Omit the last two digits of the score.

    Args:
        total_score: The total score for 3-player mahjong.

    Raises:
        ValueError: If the total score does not match the total score
            required by the rules.
    """
    if total_score != TOTAL_SCORE_3:
        msg = f"The total score of 3-player is incorrect.: {total_score}"
        raise ValueError(msg)


def validate_total_score(total_score: int, num_player: NumPlayer) -> None:
    """Validates a total score.

    Checks if the total score matches the total score required by the
    rule of mahjong for the specified number of players.
    Omit the last two digits of the score.

    Args:
        total_score: The total score.
        num_player: The number of players.

    Raises:
        ValueError: If the total score does not match the total score
            required by the rules.
    """
    match num_player:
        case NumPlayer.FOUR:
            validate_total_score_4(total_score)
        case NumPlayer.THREE:
            validate_total_score_3(total_score)
        case unreachable:
            assert_never(unreachable)


def validate_scores(
    num_riichi_deposit: int,
    scores: Sequence[int],
    num_player: NumPlayer,
) -> None:
    """Validates scores.

    Checks if each score and its total are valid according to the rules.
    Omit the last two digits of the score.

    Args:
        num_riichi_deposit: The number riichi deposits.
        scores: The players' scores.
        num_player: The number of players.

    Raises:
        ValueError: If the number of riichi deposits is negative,
            if the number of scores does not match the number of
            players, if a score is less than 0 or greater than the total
            score of the specified number of players, or if the total
            score does not match the total score required by the rules.
    """
    if num_riichi_deposit < 0:
        msg = (
            "The number of riichi deposit must be greater than or equal to 0.:"
            f" {num_riichi_deposit}"
        )
        raise ValueError(msg)
    if len(scores) != num_player:
        msg = "The number of the scores does not match the `num_player`"
        raise ValueError(msg)
    for score in scores:
        validate_score(score, num_player)
    validate_total_score(num_riichi_deposit * 10 + sum(scores), num_player)


def validate_input_scores(
    num_riichi_deposit: int,
    input_scores: Sequence[int],
    num_player: NumPlayer,
) -> None:
    """Validates input scores.

    First checks if the last two digits of each input score are 0.
    Then, checks if each score and its total are valid according to the
    rules.

    Args:
        num_riichi_deposit: The number riichi deposits.
        input_scores: The input players' scores.
        num_player: The number of players.

    Raises:
        ValueError: If the last two digits of each input score are not
            0, if the number of riichi deposits is negative, if the
            number of scores does not match the number of players, if a
            score is less than 0 or greater than the total score of the
            specified number of players, or if the total score does not
            match the total score required by the rules.
    """
    scores = []
    for input_score in input_scores:
        score, mod = divmod(input_score, 100)
        if mod != 0:
            msg = f"The last two digits of score must be 0.: {input_score}"
            raise ValueError(msg)
        scores.append(score)
    validate_scores(num_riichi_deposit, scores, num_player)


def validate_round(round_: Round, game_length: GameLength) -> None:
    """Validates round.

    Checks if the round is valid for the game length.
    If the game length is Tonpu (東風), the round will be up to South 4
    (南4局). If the game length is Hanchan (半荘), the round will be up
    to West 4 (西4局).

    Args:
        round_: The round to validate.
        game_length: The length of the game.

    Raises:
        ValueError: If the round is invalid for the game length.
    """
    invalid_round = (
        Round.WEST_1 if game_length == GameLength.TONPU else (Round.WEST_4 + 1)
    )
    if round_ >= invalid_round:
        round_name = "West" if game_length == GameLength.TONPU else "North"
        msg = (
            f"In a {get_game_length_name(game_length)} game, rounds after"
            f" {round_name}-1 do not exist."
        )
        raise ValueError(msg)
