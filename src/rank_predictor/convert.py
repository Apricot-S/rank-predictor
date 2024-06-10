from dataclasses import dataclass
from enum import IntFlag
from logging import getLogger
from pathlib import Path

from defusedxml import ElementTree

from rank_predictor.rank import classify
from rank_predictor.types import (
    DataName,
    GameLength,
    NumPlayer,
    get_game_length_name,
)

logger = getLogger(__name__)


class _GameType(IntFlag):
    IS_HANCHAN = 0x008
    IS_THREE_PLAYER = 0x010


@dataclass
class _RoundState:
    round_: int
    num_counter_stick: int
    num_riichi_deposit: int


def _create_header(
    num_player: NumPlayer,
    *,
    output_final_score: bool,
    output_filename: bool,
) -> str:
    header = (
        f"{DataName.ROUND},{DataName.NUM_COUNTER_STICK},"
        f"{DataName.NUM_RIICHI_DEPOSIT},"
        + ",".join(f"{DataName.SCORE}_{i}" for i in range(num_player))
        + f",{DataName.RANK_CLASS}"
    )

    if output_final_score:
        header += "," + ",".join(f"final_score_{i}" for i in range(num_player))

    if output_filename:
        header += ",filename"

    header += "\n"
    return header


def _parse_game_type(game_type: int) -> tuple[NumPlayer, GameLength]:
    num_player = (
        NumPlayer.THREE
        if game_type & _GameType.IS_THREE_PLAYER
        else NumPlayer.FOUR
    )
    game_length = (
        GameLength.HANCHAN
        if game_type & _GameType.IS_HANCHAN
        else GameLength.TONPU
    )
    return (num_player, game_length)


def _parse_seed(seed: str) -> _RoundState | None:
    seed_list = seed.split(",")
    if len(seed_list) != 6:  # noqa: PLR2004
        logger.warning("The number of `seed` is invalid.: %s", seed_list)
        return None

    try:
        seed_numbers = [int(x) for x in seed_list]
    except ValueError:
        logger.warning(
            "`seed` contains non-numeric characters.: %s",
            seed_list,
        )
        return None

    round_ = seed_numbers[0]
    if round_ < 0 or round_ > 11:  # noqa: PLR2004
        logger.warning("The number of round is invalid.: %s", round_)
        return None

    num_counter_stick = seed_numbers[1]
    if num_counter_stick < 0:
        logger.warning(
            "The number of counter sticks is invalid.: %s",
            num_counter_stick,
        )
        return None

    num_riichi_deposit = seed_numbers[2]
    if num_riichi_deposit < 0:
        logger.warning(
            "The number of riichi deposits is invalid.: %s",
            num_riichi_deposit,
        )
        return None

    return _RoundState(
        round_=round_,
        num_counter_stick=num_counter_stick,
        num_riichi_deposit=num_riichi_deposit,
    )


def _parse_score(score: str, num_player: NumPlayer) -> list[int] | None:
    score_list = score.split(",")

    # Even in the case of 3-player, there are 4 scores in `ten`.
    # example: ten="350,350,350,0"  # noqa: ERA001
    if len(score_list) != NumPlayer.FOUR:
        logger.warning("The number of `ten` is invalid.: %s", score_list)
        return None

    if num_player == NumPlayer.THREE:
        score_list.pop(3)

    try:
        score_numbers = [int(x) for x in score_list]
    except ValueError:
        logger.warning(
            "`ten` contains non-numeric characters.: %s",
            score_list,
        )
        return None

    if any(p < 0 for p in score_numbers):
        logger.warning(
            "A negative score is included at the start of the round.: %s",
            score_numbers,
        )
        return None

    return score_numbers


def _parse_result(result: str, num_player: NumPlayer) -> list[int] | None:
    result_list = result.split(",")

    # Even in the case of 3-player, there are 4 scores in `owari`.
    # example: owari="400,0.0,-63,-66.0,713,66.0,0,0.0"  # noqa: ERA001
    if len(result_list) != (NumPlayer.FOUR * 2):
        logger.warning("The number of `owari` is invalid.: %s", result_list)
        return None

    score_list = result_list[::2]

    if num_player == NumPlayer.THREE:
        score_list.pop(3)

    try:
        score_numbers = [int(x) for x in score_list]
    except ValueError:
        logger.warning(
            "The scores of `owari` contains non-numeric characters.: %s",
            result_list,
        )
        return None

    return score_numbers


def _create_line(
    state: _RoundState,
    score: list[int],
    result: list[int],
    game_record_file: Path | None,
    *,
    output_final_score: bool,
) -> str:
    rank_class = classify(result)
    line = (
        f"{state.round_},{state.num_counter_stick},{state.num_riichi_deposit},"
        f"{','.join(map(str, score))},"
        f"{rank_class}"
    )

    if output_final_score:
        line += f",{','.join(map(str, result))}"

    if game_record_file is not None:
        line += f",{game_record_file.name}"

    line += "\n"
    return line


def convert(
    num_player: NumPlayer,
    game_length: GameLength,
    game_record_dir: Path,
    game_record_extension: str,
    annotated_data: Path,
    *,
    output_final_score: bool,
    output_filename: bool,
) -> None:
    if not game_record_dir.is_dir():
        msg = f"`game_record_dir` is not directory: {game_record_dir}"
        raise FileNotFoundError(msg)

    if annotated_data.is_dir():
        msg = (
            "A directory with the same name as `annotated_data` exists:"
            f" {annotated_data}"
        )
        raise FileExistsError(msg)

    logger.info(
        "Conversion target: %s-Player, %s",
        num_player,
        get_game_length_name(game_length),
    )

    header = _create_header(
        num_player,
        output_final_score=output_final_score,
        output_filename=output_filename,
    )
    with annotated_data.open("w") as f:
        f.write(header)

    for file in game_record_dir.glob(
        f"*.{game_record_extension}",
        case_sensitive=True,
    ):
        logger.info("Parsing... : %s", file.name)
        tree = ElementTree.parse(file)
        root = tree.getroot()

        if root.tag != "mjloggm":
            logger.warning("This file is not in mjlog format.")
            continue

        go = root.find("GO")
        if go is None:
            logger.warning("`GO` tag is not included.")
            continue

        game_type = go.get("type")
        if not isinstance(game_type, str):
            logger.warning("`GO` tag is missing a `type` attribute.")
            continue

        try:
            game_type = int(game_type)
        except ValueError:
            logger.warning("`type` is not a number.: %s", game_type)
            continue

        log_num_player, log_game_length = _parse_game_type(game_type)
        if (log_num_player != num_player) or (log_game_length != game_length):
            logger.info(
                "This mjlog is not a target.: %s-Player, %s",
                log_num_player,
                get_game_length_name(log_game_length),
            )
            continue

        inits = root.findall("INIT")
        if not inits:
            logger.warning("`INIT` tag is not included.")
            continue

        states: list[_RoundState] = []
        scores: list[list[int]] = []
        continue_ = False
        for init in inits:
            seed = init.get("seed")
            if not isinstance(seed, str):
                logger.warning("`INIT` tag is missing a `seed` attribute.")
                continue_ = True
                break

            state = _parse_seed(seed)
            if state is None:
                continue_ = True
                break

            ten = init.get("ten")
            if not isinstance(ten, str):
                logger.warning("`INIT` tag is missing a `ten` attribute.")
                continue_ = True
                break

            score = _parse_score(ten, log_num_player)
            if score is None:
                continue_ = True
                break

            states.append(state)
            scores.append(score)

        if continue_:
            continue

        owari = None
        agaris = root.findall("AGARI")
        owari = agaris[-1].get("owari")
        if owari is None:
            ryuukyokus = root.findall("RYUUKYOKU")
            owari = ryuukyokus[-1].get("owari")

        if owari is None:
            logger.warning("There is no score at the end of the game.")
            continue

        result = _parse_result(owari, log_num_player)
        if result is None:
            continue

        with annotated_data.open("a") as f:
            for st, sc in zip(states, scores, strict=True):
                line = _create_line(
                    st,
                    sc,
                    result,
                    file if output_filename else None,
                    output_final_score=output_final_score,
                )
                f.write(line)

    logger.info("Conversion is complete.")
