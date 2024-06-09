import pickle
from pathlib import Path

import numpy as np
import polars as pl
from sklearn.linear_model import LogisticRegression

from rank_predictor.types import GameLength, NumPlayer


def train(
    num_player: NumPlayer,
    game_length: GameLength,
    config: Path,
    training_data: Path,
    model: Path,
) -> None:
    if not config.is_file():
        msg = f"`config` file is not found.: {config}"
        raise FileNotFoundError(msg)

    if not training_data.is_file():
        msg = f"`training_data` file is not found.: {training_data}"
        raise FileNotFoundError(msg)

    if model.is_dir():
        msg = f"`model` exists as the directory.: {model}"
        raise FileExistsError(msg)

    df = pl.read_csv(training_data)
