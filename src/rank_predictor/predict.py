import pickle
from pathlib import Path

import polars as pl

from rank_predictor.types import NumPlayer, ProbabilityMatrix, Round, Scores


def predict(
    num_player: NumPlayer,
    round: Round,
    num_counter_stick: int,
    num_riichi_deposit: int,
    score: Scores,
    model: Path,
) -> ProbabilityMatrix:
    return (
        (0.25, 0.25, 0.25, 0.25),
        (0.25, 0.25, 0.25, 0.25),
        (0.25, 0.25, 0.25, 0.25),
        (0.25, 0.25, 0.25, 0.25),
    )


def calculate_average_rank(
    matrix: ProbabilityMatrix,
) -> tuple[float, float, float, float] | tuple[float, float, float]:
    return (2.5, 2.5, 2.5, 2.5)
