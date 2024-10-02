from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass(unsafe_hash=True)
class ActionBuyFood(Action):
    shop_index: int
    pet_position: int
