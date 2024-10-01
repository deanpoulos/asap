from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionBuyAndMergePet(Action):
    shop_index: int
    pet_position: int
