from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Self

import numpy as np
import polars as pl
from sklearn.linear_model import LogisticRegression

from rank_predictor.types import (
    GameLength,
    NumPlayer,
    get_game_length_name,
    validate_game_length,
    validate_num_player,
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
) -> object:
    validate_num_player(num_player)
    validate_game_length(game_length)

    logger.info(
        "Training target: %s-Player, %s",
        num_player,
        get_game_length_name(game_length),
    )

    clf = LogisticRegression()

    return object()
