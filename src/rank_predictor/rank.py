"""Provides functionality for rank classification."""

from collections.abc import Sequence
from itertools import permutations
from typing import Final

from rank_predictor.types import NumPlayer

RANK_PERMUTATION_4: Final = tuple(permutations(range(NumPlayer.FOUR)))
RANK_PERMUTATION_3: Final = tuple(permutations(range(NumPlayer.THREE)))


def get_indexes(
    num_player: NumPlayer,
    player: int,
    rank: int,
) -> tuple[int, ...]:
    """Retrieves the indexes of the rank permutations.

    Args:
        num_player: The number of players.
        player: The index of the player whose rank is to be found.
            Index is 0-based.
        rank: The rank to find within the permutations. Rank is 0-based.

    Returns:
        Indexes of permutations where the player's rank is equal to the
            specified rank.

    Raises:
        IndexError: If `player` of `rank` is out of the valid range
            based on `num_player`.
    """
    if not (0 <= player < num_player):
        msg = (
            f"Player index {player} is out of range for {num_player}-players."
        )
        raise IndexError(msg)
    if not (0 <= rank < num_player):
        msg = f"Rank {rank} is out of range for {num_player}-players."
        raise IndexError(msg)

    rank_permutation = (
        RANK_PERMUTATION_4
        if num_player == NumPlayer.FOUR
        else RANK_PERMUTATION_3
    )
    return tuple(
        i for i, t in enumerate(rank_permutation) if t[rank] == player
    )


RANK_CLASS_4: Final = {
    "".join(map(str, p)): i
    for i, p in enumerate(permutations(range(NumPlayer.FOUR)))
}
RANK_CLASS_3: Final = {
    "".join(map(str, p)): i
    for i, p in enumerate(permutations(range(NumPlayer.THREE)))
}


def classify(scores: Sequence[int]) -> int:
    """Classifies the rank of players based on their scores.

    It sorts the scores in descending order and maps the sorted indexes
    to the corresponding rank permutation.

    Args:
        scores: The scores of players.

    Returns:
        The index of rank permutation that corresponds to the scores.

    Raises:
        ValueError: If the number of scores provided does not match the
            expected number of players (4 or 3).
    """
    num_player = len(scores)
    if num_player not in NumPlayer:
        msg = f"The number of scores is invalid.: {num_player}"
        raise ValueError(msg)

    # Sort the scores and get the indices in descending order
    sorted_indices = sorted(
        range(num_player),
        key=lambda i: scores[i],
        reverse=True,
    )

    sorted_indices_str = "".join(map(str, sorted_indices))

    if num_player == NumPlayer.FOUR:
        return RANK_CLASS_4[sorted_indices_str]
    return RANK_CLASS_3[sorted_indices_str]
