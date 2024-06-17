from collections.abc import Sequence

import numpy as np
import polars as pl

from rank_predictor.model import Model
from rank_predictor.rank import get_indexes
from rank_predictor.types import DataName, NumPlayer, Round


def create_feature(
    round_: Round,
    num_counter_stick: int,
    num_riichi_deposit: int,
    score: Sequence[int],
) -> pl.DataFrame:
    data: dict[str, list[int]] = {
        DataName.ROUND: [round_],
        DataName.NUM_COUNTER_STICK: [num_counter_stick],
        DataName.NUM_RIICHI_DEPOSIT: [num_riichi_deposit],
    }
    for i, s in enumerate(score):
        data[f"{DataName.SCORE}_{i}"] = [s]
    return pl.DataFrame(data)


def predict_proba(model: Model, feature: pl.DataFrame) -> np.ndarray:
    return model.classifier.predict_proba(feature)[0]


def calculate_player_rank_proba(
    num_player: NumPlayer,
    proba: np.ndarray,
) -> np.ndarray:
    player_rank_proba = np.zeros((num_player, num_player))
    for player in range(num_player):
        for rank in range(num_player):
            indexes = get_indexes(num_player, player, rank)
            player_rank_proba[player, rank] += sum(proba[i] for i in indexes)
    return player_rank_proba


def calculate_expected_rank(player_rank_proba: np.ndarray) -> np.ndarray:
    ranks = np.arange(1, player_rank_proba.shape[1] + 1)
    return np.sum(player_rank_proba * ranks, axis=1)
