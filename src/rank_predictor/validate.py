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
        if not column_data.is_integer():
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


def validate_score_4(score: int) -> None:
    if score < 0 or score > TOTAL_SCORE_4:
        msg = f"The score for 4-player is incorrect.: {score}"
        raise ValueError(msg)


def validate_score_3(score: int) -> None:
    if score < 0 or score > TOTAL_SCORE_3:
        msg = f"The score for 3-player is incorrect.: {score}"
        raise ValueError(msg)


def validate_score(score: int, num_player: NumPlayer) -> None:
    match num_player:
        case NumPlayer.FOUR:
            validate_score_4(score)
        case NumPlayer.THREE:
            validate_score_3(score)
        case unreachable:
            assert_never(unreachable)


def validate_total_score_4(total_score: int) -> None:
    if total_score != TOTAL_SCORE_4:
        msg = f"The total score of 4-player is incorrect.: {total_score}"
        raise ValueError(msg)


def validate_total_score_3(total_score: int) -> None:
    if total_score != TOTAL_SCORE_3:
        msg = f"The total score of 3-player is incorrect.: {total_score}"
        raise ValueError(msg)


def validate_total_score(total_score: int, num_player: NumPlayer) -> None:
    match num_player:
        case NumPlayer.FOUR:
            validate_total_score_4(total_score)
        case NumPlayer.THREE:
            validate_total_score_3(total_score)
        case unreachable:
            assert_never(unreachable)


def validate_scores(scores: Sequence[int], num_player: NumPlayer) -> None:
    if len(scores) != num_player:
        msg = "The number of the scores does not match the `num_player`"
        raise ValueError(msg)
    for score in scores:
        validate_score(score, num_player)
    validate_total_score(sum(scores), num_player)


def validate_input_scores(
    input_scores: Sequence[int],
    num_player: NumPlayer,
) -> None:
    scores = []
    for input_score in input_scores:
        score, mod = divmod(input_score, 100)
        if mod != 0:
            msg = f"The last two digits of score must be 0.: {input_score}"
            raise ValueError(msg)
        scores.append(score)
    validate_scores(scores, num_player)


def validate_input_probability(probability: float) -> None:
    if probability < 0.0 or probability > 1.0:
        msg = f"Invalid probability is input.: {probability}"
        raise ValueError(msg)
