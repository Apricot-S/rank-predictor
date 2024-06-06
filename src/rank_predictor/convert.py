from enum import IntFlag
from logging import getLogger
from pathlib import Path
from typing import Final

from defusedxml import ElementTree

from rank_predictor.types import GameLength, NumPlayer

logger = getLogger(__name__)

MJLOG_ROOT_TAG: Final = "mjloggm"


class TenhouGameType(IntFlag):
    IS_HANCHAN = 0x008
    IS_THREE_PLAYER = 0x010


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

    for file in game_record_dir.glob("*.xml"):
        tree = ElementTree.parse(file)
        root = tree.getroot()

        if root.tag != MJLOG_ROOT_TAG:
            logger.warning("This file is not in mjlog format.: %s", file.name)
            continue

        go = root.find("GO")
        if go is None:
            logger.warning("`GO` tag is not included.: %s", file.name)
            continue

        game_type = go.attrib.get("type")
        if not isinstance(game_type, str):
            logger.warning(
                "`GO` tag is missing a `type` attribute.: %s",
                file.name,
            )
            continue

        try:
            game_type = int(game_type)
        except ValueError:
            logger.warning("`type` is not a number.: %s", game_type)
            continue

        log_num_player = (
            NumPlayer.THREE
            if bool(game_type & TenhouGameType.IS_THREE_PLAYER)
            else NumPlayer.FOUR
        )
        if log_num_player != num_player:
            logger.info("This mjlog is not a target.: %s", log_num_player)
            continue

        log_game_length = (
            GameLength.HANCHAN
            if bool(game_type & TenhouGameType.IS_HANCHAN)
            else GameLength.TONPU
        )
        if log_game_length != game_length:
            logger.info("This mjlog is not a target.: %s", log_game_length)
            continue
