import numpy as np

from asap.training.opponents.opponent import Opponent
from asap.training.opponents.self_play.adversary_loader import OpponentLoader


class OpponentSelfPlay(Opponent):
    def __init__(self, loader: OpponentLoader):
        self.model = None
        self.loader = loader

    def initialize(self):
        self.model = self.loader.load()

    def make_action(self, observation, action_mask: np.ndarray):
        if self.model is None:
            raise AttributeError('Model is not initialized. Did you call `initialize()`?')

        return self.model.predict(observation, deterministic=True, action_masks=action_mask)
