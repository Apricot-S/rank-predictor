from typing import Final, assert_never

from rank_predictor.types import NumPlayer

MAX_INPUT_SCORE_4: Final[int] = 1_000
MAX_INPUT_SCORE_3: Final[int] = 1_050


def validate_input_score_4(score: int) -> None:
    if score < 0 or score > MAX_INPUT_SCORE_4:
        msg = f"Invalid score is input. : {score}"
        raise ValueError(msg)


def validate_input_score_3(score: int) -> None:
    if score < 0 or score > MAX_INPUT_SCORE_3:
        msg = f"Invalid score is input. : {score}"
        raise ValueError(msg)


def validate_input_score(score: int, num_player: NumPlayer) -> None:
    match num_player:
        case NumPlayer.FOUR:
            validate_input_score_4(score)
        case NumPlayer.THREE:
            validate_input_score_3(score)
        case unreachable:
            assert_never(unreachable)


def validate_input_probability(probability: float) -> None:
    if probability < 0.0 or probability > 1.0:
        msg = f"Invalid probability is input. : {probability}"
        raise ValueError(msg)
