from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionBuyFood(Action):
    shop_index: int
    pet_position: int
