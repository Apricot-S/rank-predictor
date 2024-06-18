"""Provides functionality to train model."""

from logging import getLogger

import polars as pl

from rank_predictor.model import Classifier, Model
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
    training_data: pl.DataFrame,
    classifier: Classifier,
) -> Model:
    """Trains a model using the provided classifier and training data.

    This function utilizes specific features and a label from
    `training_data`. The features include `round`, `num_counter_stick`,
    `num_riichi_deposit`, and `score_*`. Here, * depends on the number
    of players. For a 4-player, * takes values from 0 to 3, and for a
    3-player, * takes values from 0 to 2. The label used is
    `rank_class`.

    Args:
        num_player: The number of players.
        game_length: The length of the game.
        training_data: The data used for training the model
            which includes features and labels.
        classifier: The machine learning classifier used to train.

    Returns:
        An instance of a trained model that is ready to make
            predictions.

    Raises:
        ValueError: If the `training_data` is invalid.
    """
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
    classifier.fit(feature, label)

    logger.info("Training is complete.")

    return Model(num_player, game_length, classifier)
