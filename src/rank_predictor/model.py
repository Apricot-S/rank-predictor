"""Provides classes for classifier model."""

# ruff: noqa: N803

from typing import Protocol, Self

import numpy as np

from rank_predictor.types import GameLength, NumPlayer


class Classifier(Protocol):
    """Protocol for classes that conform to scikit-learn's classifier.

    Requires implementation of `fit` and `predict_proba` methods.
    """

    def fit(self, X: np.ndarray, y: np.ndarray, *args, **kwargs) -> Self:
        """Fits the model according to the given training data.

        Args:
            X: The features of the training data.
            y: The target labels for the training data.
            *args: Optional arguments.
            **kwargs: Optional keyword arguments.

        Returns:
            A fitted classifier.
        """
        ...

    def predict_proba(self, X: np.ndarray, *args, **kwargs) -> np.ndarray:
        """Predict the probabilities of each class.

        Args:
            X: The features of the data to predict.
            *args: Optional arguments.
            **kwargs: Optional keyword arguments.

        Returns:
            An array containing the probabilities of each class.
        """
        ...


class Model:
    """The classifier model used to predict the rank class.

    For more information on rank classes, refer to
    `rank_predictor.rank.RANK_CLASS_4` and
    `rank_predictor.rank.RANK_CLASS_3`.

    Attributes:
        num_player: The number of players that the model supports.
        game_length: The length of the game that the model supports.
        classifier: The classifier to use for prediction.
    """

    def __init__(
        self,
        num_player: NumPlayer,
        game_length: GameLength,
        classifier: Classifier,
    ) -> None:
        """Initializes the instance of `Model`.

        Args:
            num_player: The number of players that the model supports.
            game_length: The length of the game that the model supports.
            classifier: The classifier to use for prediction.
        """
        self.num_player = num_player
        self.game_length = game_length
        self.classifier = classifier
