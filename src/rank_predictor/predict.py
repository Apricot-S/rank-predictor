import pickle
from pathlib import Path

import polars as pl

from rank_predictor.types import NumPlayer, ProbabilityMatrix, Round


def predict(
    num_player: NumPlayer,
    model: Path,
    round: Round,
    num_counter_stick: int,
    num_riichi_deposit: int,
    score: tuple[int, int, int, int] | tuple[int, int, int],
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
    return (0.25, 0.25, 0.25, 0.25)
