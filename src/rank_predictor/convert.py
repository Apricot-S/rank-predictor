import pickle
from enum import Flag
from pathlib import Path
from xml.etree import ElementTree

import polars as pl

from rank_predictor.types import GameLength, NumPlayer


class TenhouGameType(Flag):
    IS_TWO_WIND = 0x008
    IS_THREE_PLAYER = 0x010


def convert(
    num_player: NumPlayer,
    game_length: GameLength,
    game_record_dir: Path,
    training_data: Path,
) -> None:
    pass
