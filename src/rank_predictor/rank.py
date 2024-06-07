from itertools import permutations
from typing import Final

from rank_predictor.types import NumPlayer

RANK_CLASS_4: Final = {
    "".join(map(str, p)): i
    for i, p in enumerate(permutations(range(NumPlayer.FOUR)))
}
RANK_CLASS_3: Final = {
    "".join(map(str, p)): i
    for i, p in enumerate(permutations(range(NumPlayer.THREE)))
}


def classify(scores: list[int]) -> int:
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
