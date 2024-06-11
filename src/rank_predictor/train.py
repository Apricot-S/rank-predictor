from logging import getLogger
from typing import Any

import polars as pl
from sklearn.linear_model import LogisticRegression

from rank_predictor.types import (
    DataName,
    GameLength,
    NumPlayer,
    get_game_length_name,
)
from rank_predictor.validate import validate_annotated_data

logger = getLogger(__name__)


def train(
    num_player: NumPlayer,
    game_length: GameLength,
    hyper_parameter: dict[str, Any],
    training_data: pl.DataFrame,
) -> LogisticRegression:
    logger.info(
        "Training target: %s-Player, %s",
        num_player,
        get_game_length_name(game_length),
    )

    validate_annotated_data(num_player, game_length, training_data)

    feature_columns = [
        DataName.ROUND,
        DataName.NUM_COUNTER_STICK,
        DataName.NUM_RIICHI_DEPOSIT,
        *[f"{DataName.SCORE}_{i}" for i in range(num_player)],
    ]
    label_column = DataName.RANK_CLASS
    feature = training_data.select(feature_columns)
    label = training_data.select(label_column).to_series()

    clf = LogisticRegression(**hyper_parameter)
    clf.fit(feature, label)

    logger.info("Training is complete.")

    return clf
