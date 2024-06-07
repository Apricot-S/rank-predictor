import argparse
from logging import INFO, Formatter, StreamHandler, basicConfig
from pathlib import Path

from rank_predictor.types import GameLength, NumPlayer

LOG_LEVEL = INFO

stream_handler = StreamHandler()
stream_handler.setLevel(LOG_LEVEL)

formatter = Formatter("%(message)s")
stream_handler.setFormatter(formatter)

basicConfig(level=LOG_LEVEL, handlers=[stream_handler])


def convert() -> int:
    import rank_predictor.convert

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "num_player",
        type=int,
        choices=(4, 3),
    )
    parser.add_argument(
        "game_length",
        choices=(GameLength.TONPU, GameLength.HANCHAN),
    )
    parser.add_argument(
        "game_record_dir",
        type=str,
    )
    parser.add_argument(
        "game_record_extension",
        type=str,
    )
    parser.add_argument(
        "training_data",
        type=str,
    )
    args = parser.parse_args()

    num_player = NumPlayer(args.num_player)
    game_length = GameLength(args.game_length)
    game_record_dir = Path(args.game_record_dir)
    game_record_extension: str = args.game_record_extension
    training_data = Path(args.training_data)

    rank_predictor.convert.convert(
        num_player,
        game_length,
        game_record_dir,
        game_record_extension,
        training_data,
    )
    return 0


def train() -> int:
    import rank_predictor.train

    return 0


def predict() -> int:
    import rank_predictor.predict

    return 0
