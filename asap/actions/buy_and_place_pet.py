from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionBuyAndPlacePet(Action):
    shop_index: int
    pet_position: int
