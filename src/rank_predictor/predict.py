from collections.abc import Sequence

import numpy as np
import polars as pl
from sklearn.linear_model import LogisticRegression

from rank_predictor.model import Model
from rank_predictor.types import DataName, ProbabilityMatrix, Round


def predict_proba(
    model: Model,
    round_: Round,
    num_counter_stick: int,
    num_riichi_deposit: int,
    score: Sequence[int],
) -> np.ndarray:
    data: dict[str, list[int]] = {
        DataName.ROUND: [round_],
        DataName.NUM_COUNTER_STICK: [num_counter_stick],
        DataName.NUM_RIICHI_DEPOSIT: [num_riichi_deposit],
    }
    for i, s in enumerate(score):
        data[f"{DataName.SCORE}_{i}"] = [s]
    feature = pl.DataFrame(data)

    assert isinstance(model.clf, LogisticRegression)  # noqa: S101
    return model.clf.predict_proba(feature)[0]  # type: ignore[reportArgumentType]


def calculate_average_rank(
    matrix: ProbabilityMatrix,
) -> tuple[float, float, float, float] | tuple[float, float, float]:
    return (2.5, 2.5, 2.5, 2.5)
