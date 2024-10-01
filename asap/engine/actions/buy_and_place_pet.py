from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionBuyAndPlacePet(Action):
    shop_index: int
    pet_position: int
