from collections.abc import Sequence

from rank_predictor.model import Model
from rank_predictor.types import (
    GameLength,
    NumPlayer,
    ProbabilityMatrix,
    Round,
)


def predict_proba(
    num_player: NumPlayer,
    game_length: GameLength,
    round: Round,
    num_counter_stick: int,
    num_riichi_deposit: int,
    score: Sequence[int],
    model: Model,
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
