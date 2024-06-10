from logging import NullHandler, getLogger

from rank_predictor.types import GameLength, NumPlayer

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "GameLength",
    "NumPlayer",
]
