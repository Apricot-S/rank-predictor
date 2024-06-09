from logging import getLogger

import numpy as np
import polars as pl
from sklearn.linear_model import LogisticRegression

from rank_predictor.types import GameLength, NumPlayer

logger = getLogger(__name__)


class Config:
    def __init__(self) -> None:
        pass


def train(
    num_player: NumPlayer,
    game_length: GameLength,
    config: Config,
    training_data: pl.DataFrame,
) -> object:
    if num_player not in NumPlayer:
        msg = f"Unsupported number of players selected: {num_player}"
        raise ValueError(msg)

    if game_length not in GameLength:
        msg = f"Unsupported game length selected: {game_length}"
        raise ValueError(msg)

    logger.info(
        "Training target: %s-Player, %s",
        num_player,
        "Tonpu" if game_length == GameLength.TONPU else "Hanchan",
    )

    clf = LogisticRegression()

    return object()
