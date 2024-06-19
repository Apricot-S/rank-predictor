"""Provides functionality to predict expected final rank."""

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
    """Creates a features based on the current state of a round.

    Args:
        round_: The current round.
        num_counter_stick: The number of counter sticks.
        num_riichi_deposit: The number of riichi deposits.
        score: The current scores of the players.

    Returns:
        A DataFrame containing the features.
    """
    data: dict[str, list[int]] = {
        DataName.ROUND: [round_],
        DataName.NUM_COUNTER_STICK: [num_counter_stick],
        DataName.NUM_RIICHI_DEPOSIT: [num_riichi_deposit],
    }
    for i, s in enumerate(score):
        data[f"{DataName.SCORE}_{i}"] = [s]
    return pl.DataFrame(data)


def predict_proba(model: Model, feature: pl.DataFrame) -> np.ndarray:
    """Predicts the probabilities of each rank class.

    For more information on rank classes, refer to
    `rank_predictor.rank.RANK_CLASS_4` and
    `rank_predictor.rank.RANK_CLASS_3`.

    Args:
        model: The model to use for prediction.
        feature: The features to use as input for prediction.

    Returns:
        An array of the probabilities of each rank class.
    """
    return model.classifier.predict_proba(feature)[0]


def calculate_player_rank_proba(
    num_player: NumPlayer,
    proba: np.ndarray,
) -> np.ndarray:
    """Calculates the probabilities of each player's rank.

    Args:
        num_player: The number of players.
        proba: The probabilities of each rank class.

    Returns:
        An array of the probabilities of each player's rank.

    Examples:
        >>> proba = np.array(
        ...     [
        ...         0.2083811,
        ...         0.04574999,
        ...         0.13748033,
        ...         0.22065941,
        ...         0.22998391,
        ...         0.15774526,
        ...     ]
        ... )
        >>> player_rank_proba = calculate_player_rank_proba(
        ...     NumPlayer.THREE,
        ...     proba,
        ... )
        >>> print(player_rank_proba)
        [[0.2541311  0.36746423 0.37840467]
         [0.35813974 0.36612636 0.2757339 ]
         [0.38772917 0.26640941 0.34586143]]
    """
    player_rank_proba = np.zeros((num_player, num_player))
    for player in range(num_player):
        for rank in range(num_player):
            indexes = get_indexes(num_player, player, rank)
            player_rank_proba[player, rank] += sum(proba[i] for i in indexes)
    return player_rank_proba


def calculate_expected_rank(player_rank_proba: np.ndarray) -> np.ndarray:
    """Calculates the expected rank of each player.

    Args:
        player_rank_proba: The probabilities of each player's rank.

    Returns:
        An array of the expected ranks of each player.

    Examples:
        >>> player_rank_proba = np.array(
        ...     [
        ...         [0.25413110, 0.36746423, 0.37840467],
        ...         [0.35813974, 0.36612636, 0.27573390],
        ...         [0.38772917, 0.26640941, 0.34586143],
        ...     ]
        ... )
        >>> expected_ranks = calculate_expected_rank(player_rank_proba)
        >>> print(expected_ranks)
        [2.12427357 1.91759416 1.95813226]
    """
    ranks = np.arange(1, player_rank_proba.shape[1] + 1)
    return np.sum(player_rank_proba * ranks, axis=1)
