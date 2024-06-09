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
        type=Path,
    )
    parser.add_argument(
        "game_record_extension",
    )
    parser.add_argument(
        "annotated_data",
        type=Path,
    )
    parser.add_argument(
        "-f",
        "--final-score",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--filename",
        action="store_true",
    )
    args = parser.parse_args()

    num_player = NumPlayer(args.num_player)
    game_length = GameLength(args.game_length)

    rank_predictor.convert.convert(
        num_player,
        game_length,
        args.game_record_dir,
        args.game_record_extension,
        args.annotated_data,
        output_final_score=args.final_score,
        output_filename=args.filename,
    )
    return 0


def split() -> int:
    import rank_predictor.split

    def int_or_float(arg: str) -> int | float:
        try:
            return int(arg)
        except ValueError:
            try:
                return float(arg)
            except ValueError:
                msg = f"invalid int or float value: '{arg}'"
                raise argparse.ArgumentTypeError(msg) from None

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_data_path",
        type=Path,
    )
    parser.add_argument(
        "train_data_path",
        type=Path,
    )
    parser.add_argument(
        "test_data_path",
        type=Path,
    )
    parser.add_argument(
        "--test_size",
        type=int_or_float,
    )
    parser.add_argument(
        "--train_size",
        type=int_or_float,
    )
    parser.add_argument(
        "-r",
        "--random_state",
        type=int,
    )
    parser.add_argument(
        "-f",
        "--shuffle-false",
        action="store_true",
    )
    args = parser.parse_args()

    rank_predictor.split.split(
        args.input_data_path,
        args.train_data_path,
        args.test_data_path,
        args.test_size,
        args.train_size,
        args.random_state,
        shuffle=(not args.shuffle_false),
    )
    return 0


def train() -> int:
    import rank_predictor.train

    return 0


def predict() -> int:
    import rank_predictor.predict

    return 0
