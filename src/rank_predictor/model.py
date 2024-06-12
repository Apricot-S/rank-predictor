from sklearn.base import BaseEstimator

from rank_predictor.types import GameLength, NumPlayer


class Model:
    def __init__(
        self,
        num_player: NumPlayer,
        game_length: GameLength,
        clf: BaseEstimator,
    ) -> None:
        self.num_player = num_player
        self.game_length = game_length
        self.clf = clf
