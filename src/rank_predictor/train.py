from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Self

import polars as pl
from sklearn.linear_model import LogisticRegression

from rank_predictor.types import (
    DataName,
    GameLength,
    NumPlayer,
    Round,
    get_game_length_name,
)

logger = getLogger(__name__)


@dataclass
class Config:
    @classmethod
    def from_file(cls, file: Path) -> Self:
        if not file.is_file():
            msg = f"`file` is not a file: {file}"
            raise FileNotFoundError(msg)

        return cls()


def train(
    num_player: NumPlayer,
    game_length: GameLength,
    config: Config,
    training_data: pl.DataFrame,
) -> LogisticRegression:
    logger.info(
        "Training target: %s-Player, %s",
        num_player,
        get_game_length_name(game_length),
    )

    feature_columns = [
        DataName.ROUND,
        DataName.NUM_COUNTER_STICK,
        DataName.NUM_RIICHI_DEPOSIT,
        *[f"{DataName.SCORE}_{i}" for i in range(num_player)],
    ]
    label_column = DataName.RANK_CLASS

    required_columns = [*feature_columns, label_column]
    columns = training_data.columns
    missing_columns = [r for r in required_columns if r not in columns]
    if missing_columns:
        msg = f"Training data is missing columns: {missing_columns}"
        raise ValueError(msg)

    if (num_player == NumPlayer.THREE) and (f"{DataName.SCORE}_3" in columns):
        msg = (
            "The training target is 3-player,"
            f" but the data contains `{DataName.SCORE}_3`."
        )
        raise ValueError(msg)

    invalid_round = (
        Round.WEST_1 if game_length == GameLength.TONPU else (Round.WEST_4 + 1)
    )
    num_invalid_round = (
        training_data.lazy()
        .filter(pl.col(DataName.ROUND) >= invalid_round)
        .select(pl.len())
        .collect()
        .item()
    )
    if num_invalid_round > 0:
        round_name = "West" if game_length == GameLength.TONPU else "North"
        msg = (
            f"The training target is {get_game_length_name(game_length)},"
            f" but the data contains rounds after {round_name}-1."
        )
        raise ValueError(msg)

    def validate_no_negative_values(column: str) -> None:
        negative_count = (
            training_data.lazy()
            .filter(pl.col(column) < 0)
            .select(pl.len())
            .collect()
            .item()
        )
        if negative_count > 0:
            msg = f"`{column}` data contains negative values."
            raise ValueError(msg)

    validate_no_negative_values(DataName.ROUND)
    validate_no_negative_values(DataName.NUM_COUNTER_STICK)
    validate_no_negative_values(DataName.NUM_RIICHI_DEPOSIT)
    for i in range(num_player):
        validate_no_negative_values(f"{DataName.SCORE}_{i}")

    feature = training_data.select(feature_columns)
    label = training_data.select(label_column).to_series()

    clf = LogisticRegression()
    clf.fit(feature, label)

    logger.info("Training is complete.")

    return clf
