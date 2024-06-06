from dataclasses import dataclass
from enum import IntFlag
from logging import getLogger
from pathlib import Path

from defusedxml import ElementTree

from rank_predictor.types import GameLength, NumPlayer

logger = getLogger(__name__)


class TenhouGameType(IntFlag):
    IS_HANCHAN = 0x008
    IS_THREE_PLAYER = 0x010


@dataclass
class RoundState:
    round_: int
    num_counter_stick: int
    num_riichi_deposit: int


def parse_game_type(game_type: int) -> tuple[NumPlayer, GameLength]:
    num_player = (
        NumPlayer.THREE
        if game_type & TenhouGameType.IS_THREE_PLAYER
        else NumPlayer.FOUR
    )
    game_length = (
        GameLength.HANCHAN
        if game_type & TenhouGameType.IS_HANCHAN
        else GameLength.TONPU
    )
    return (num_player, game_length)


def parse_seed(seed: str) -> RoundState | None:
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

    return RoundState(
        round_=round_,
        num_counter_stick=num_counter_stick,
        num_riichi_deposit=num_riichi_deposit,
    )


def parse_score(score: str, num_player: NumPlayer) -> list[int] | None:
    score_list = score.split(",")
    if len(score_list) != num_player:
        logger.warning("The number of `ten` is invalid.: %s", score_list)
        return None

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


def parse_result(result: str, num_player: NumPlayer) -> list[int] | None:
    result_list = result.split(",")
    if len(result_list) != (num_player * 2):
        logger.warning("The number of `owari` is invalid.: %s", result_list)
        return None

    score_list = result_list[::2]

    try:
        score_numbers = [int(x) for x in score_list]
    except ValueError:
        logger.warning(
            "The scores of `owari` contains non-numeric characters.: %s",
            result_list,
        )
        return None

    return score_numbers


def convert(
    num_player: NumPlayer,
    game_length: GameLength,
    game_record_dir: Path,
    training_data: Path,
) -> None:
    if not game_record_dir.is_dir():
        msg = f"`game_record_dir` is not directory: {game_record_dir}"
        raise FileNotFoundError(msg)

    if training_data.is_dir():
        msg = (
            "A directory with the same name as `training_data` exists:"
            f" {training_data}"
        )
        raise FileExistsError(msg)

    if num_player not in NumPlayer:
        msg = f"Unsupported number of players selected: {num_player}"
        raise ValueError(msg)

    match game_length:
        case GameLength.TONPU:
            length_name = "Tonpu"
        case GameLength.HANCHAN:
            length_name = "Hanchan"
        case unsupported_length:
            msg = f"Unsupported game length selected: {unsupported_length}"
            raise ValueError(msg)

    logger.info("Conversion target: %s-Player, %s", num_player, length_name)

    with training_data.open("w") as f:
        f.write(
            "round,num_counter_stick,num_riichi_deposit,"
            "current_score_0,current_score_1,current_score_2,current_score_3,"
            "final_score_0,final_score_1,final_score_2,final_score_3\n",
        )

    for file in game_record_dir.glob("*.xml"):
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

        log_num_player, log_game_length = parse_game_type(game_type)
        if log_num_player != num_player:
            logger.info("This mjlog is not a target.: %s", log_num_player)
            continue
        if log_game_length != game_length:
            logger.info("This mjlog is not a target.: %s", log_game_length)
            continue

        inits = root.findall("INIT")
        if not inits:
            logger.warning("`INIT` tag is not included.")
            continue

        states: list[RoundState] = []
        scores: list[list[int]] = []
        continue_ = False
        for init in inits:
            seed = init.get("seed")
            if not isinstance(seed, str):
                logger.warning("`INIT` tag is missing a `seed` attribute.")
                continue_ = True
                break

            state = parse_seed(seed)
            if state is None:
                continue_ = True
                break

            ten = init.get("ten")
            if not isinstance(ten, str):
                logger.warning("`INIT` tag is missing a `ten` attribute.")
                continue_ = True
                break

            score = parse_score(ten, log_num_player)
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

        result = parse_result(owari, log_num_player)
        if result is None:
            continue

        with training_data.open("a") as f:
            for st, sc in zip(states, scores, strict=True):
                f.write(f"{st.round_},")
                f.write(f"{st.num_counter_stick},")
                f.write(f"{st.num_riichi_deposit},")
                for s in sc:
                    f.write(f"{s},")
                for r in result:
                    f.write(f"{r},")
                f.write("\n")
