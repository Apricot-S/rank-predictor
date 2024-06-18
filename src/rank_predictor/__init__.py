"""Provides a framework to predict expected final rank.

Supports 4-player and 3-player mahjong.
"""

from logging import NullHandler, getLogger

from rank_predictor.types import GameLength, NumPlayer, Round

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "GameLength",
    "NumPlayer",
    "Round",
]
