from logging import NullHandler, getLogger

from rank_predictor.types import GameLength, NumPlayer, Round

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "GameLength",
    "NumPlayer",
    "Round",
]
