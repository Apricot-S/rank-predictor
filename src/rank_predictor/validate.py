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
        if annotated_data.filter(pl.col(name).is_null()).shape[0] > 0:
            msg = f"`{name}` column contains null values."
            raise ValueError(msg)

    for name in required_columns:
        if annotated_data.filter(pl.col(name) < 0).shape[0] > 0:
            msg = f"`{name}` column contains negative values."
            raise ValueError(msg)

    invalid_round = (
        Round.WEST_1 if game_length == GameLength.TONPU else (Round.WEST_4 + 1)
    )
    num_invalid_round = annotated_data.filter(
        pl.col(DataName.ROUND) >= invalid_round,
    ).shape[0]
    if num_invalid_round > 0:
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
    contains_invalid_rank_class = (
        annotated_data.filter(
            pl.col(DataName.RANK_CLASS) >= num_rank_class,
        ).shape[0]
        > 0
    )
    if contains_invalid_rank_class:
        msg = f"`{DataName.RANK_CLASS}` column contains invalid values."
        raise ValueError(msg)


def validate_score_4(score: int) -> None:
    if score < 0 or score > TOTAL_SCORE_4:
        msg = f"Invalid score is input. : {score}"
        raise ValueError(msg)


def validate_score_3(score: int) -> None:
    if score < 0 or score > TOTAL_SCORE_3:
        msg = f"Invalid score is input. : {score}"
        raise ValueError(msg)


def validate_input_score(score: int, num_player: NumPlayer) -> None:
    score = score // 100
    match num_player:
        case NumPlayer.FOUR:
            validate_score_4(score)
        case NumPlayer.THREE:
            validate_score_3(score)
        case unreachable:
            assert_never(unreachable)


def validate_input_probability(probability: float) -> None:
    if probability < 0.0 or probability > 1.0:
        msg = f"Invalid probability is input. : {probability}"
        raise ValueError(msg)
