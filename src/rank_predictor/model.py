# ruff: noqa: N803, ANN401

from typing import Any, Protocol, Self

import numpy as np

from rank_predictor.types import GameLength, NumPlayer


class Classifier(Protocol):
    def fit(self, X: Any, y: Any, *args, **kwargs) -> Self: ...

    def predict_proba(self, X: Any, *args, **kwargs) -> np.ndarray: ...


class Model:
    def __init__(
        self,
        num_player: NumPlayer,
        game_length: GameLength,
        classifier: Classifier,
    ) -> None:
        self.num_player = num_player
        self.game_length = game_length
        self.classifier = classifier
