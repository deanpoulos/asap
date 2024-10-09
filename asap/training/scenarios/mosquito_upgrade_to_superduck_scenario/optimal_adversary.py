from typing import Dict

from asap.engine.actions import ActionBuyAndPlacePet, ActionBuyAndMergePet, ActionSellPet, ActionEndTurn, Action
from asap.training.opponents.opponent import Opponent


class OpponentOptimalMosquitoUpgradeToSuperduckScenario(Opponent):
    def __init__(self, action_map_inverse: Dict[Action, int]):
        self.action_map_inverse = action_map_inverse

        self.optimal_sequence = [
            ActionBuyAndPlacePet(0, 0),
            ActionBuyAndMergePet(1, 0),
            ActionBuyAndMergePet(2, 0),
            ActionSellPet(0),
            ActionBuyAndPlacePet(0, 0),
            ActionEndTurn(),
            ActionBuyAndPlacePet(0, 1),
            ActionBuyAndMergePet(1, 1),
            ActionBuyAndMergePet(2, 1),
            ActionSellPet(1),
            ActionBuyAndPlacePet(0, 1),
            ActionEndTurn(),
        ]

    def initialize(self):
        self.sequence_index = 0

    def make_action(self, observation, action_mask):
        action = self.action_map_inverse[self.optimal_sequence[self.sequence_index]]
        self.sequence_index += 1

        return action, {}

