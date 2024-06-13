import argparse
from logging import INFO, Formatter, StreamHandler, basicConfig
from pathlib import Path

from rank_predictor.types import GameLength, NumPlayer, Round

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
    import pickle
    import tomllib

    import polars as pl

    import rank_predictor.train

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
        "training_data_path",
        type=Path,
    )
    parser.add_argument(
        "config_path",
        type=Path,
    )
    parser.add_argument(
        "model_path",
        type=Path,
    )
    args = parser.parse_args()

    num_player = NumPlayer(args.num_player)
    game_length = GameLength(args.game_length)
    training_data_path: Path = args.training_data_path
    config_path: Path = args.config_path
    model_path: Path = args.model_path

    if not training_data_path.is_file():
        msg = f"`training_data_path` is not a file: {training_data_path}"
        raise FileNotFoundError(msg)
    if not config_path.is_file():
        msg = f"`config_path` is not a file: {config_path}"
        raise FileNotFoundError(msg)

    if model_path.is_dir():
        msg = (
            "A directory with the same name as `model_path` exists:"
            f" {model_path}"
        )
        raise FileExistsError(msg)

    with config_path.open("rb") as fp:
        hyper_parameter = tomllib.load(fp)["hyper-parameter"]
    training_data = pl.read_csv(training_data_path)

    model = rank_predictor.train.train(
        num_player,
        game_length,
        training_data,
        hyper_parameter,
    )

    with model_path.open("wb") as f:
        pickle.dump(model, f)

    return 0


def predict() -> int:
    import pickle

    from rank_predictor.model import Model
    from rank_predictor.predict import (
        calculate_expected_rank,
        calculate_player_rank_proba,
        create_feature,
        predict_proba,
    )
    from rank_predictor.validate import validate_input_scores, validate_round

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
        "model_path",
        type=Path,
    )
    parser.add_argument(
        "round",
        type=int,
    )
    parser.add_argument(
        "num_counter_stick",
        type=int,
    )
    parser.add_argument(
        "num_riichi_deposit",
        type=int,
    )
    parser.add_argument(
        "score",
        type=int,
        nargs="*",
    )
    args = parser.parse_args()

    num_player = NumPlayer(args.num_player)
    game_length = GameLength(args.game_length)
    model_path: Path = args.model_path
    round_ = Round(args.round)
    num_counter_stick: int = args.num_counter_stick
    num_riichi_deposit: int = args.num_riichi_deposit
    input_score: list[int] = args.score

    validate_round(round_, game_length)
    if num_counter_stick < 0:
        msg = (
            "`num_counter_stick` must be greater than or equal to 0.:"
            f" {num_counter_stick}"
        )
        raise ValueError(msg)
    validate_input_scores(num_riichi_deposit, input_score, num_player)

    if not model_path.is_file():
        msg = f"`model_path` is not a file: {model_path}"
        raise FileNotFoundError(msg)

    with model_path.open("rb") as file:
        model = pickle.load(file)  # noqa: S301
    if not isinstance(model, Model):
        msg = "The loaded object is not an instance of `Model`."
        raise TypeError(msg)
    if model.num_player != num_player:
        msg = (
            "The `num_player` of the model does not match the provided"
            f" argument. model: {model.num_player}, argument: {num_player}"
        )
        raise ValueError(msg)
    if model.game_length != game_length:
        msg = (
            "The `game_length` of the model does not match the provided"
            f" argument. model: {model.game_length}, argument: {game_length}"
        )
        raise ValueError(msg)

    score = [s // 100 for s in input_score]
    feature = create_feature(
        round_,
        num_counter_stick,
        num_riichi_deposit,
        score,
    )
    proba = predict_proba(model, feature)
    player_rank_proba = calculate_player_rank_proba(num_player, proba)
    average_ranks = calculate_expected_rank(player_rank_proba)

    print("Rank Probability")  # noqa: T201
    for i, p in enumerate(player_rank_proba):
        print(f"player_{i}: {p}")  # noqa: T201
    print("\nExpected Rank")  # noqa: T201
    for i, a in enumerate(average_ranks):
        print(f"player_{i}: {a}")  # noqa: T201

    return 0
