from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionBuyPet(Action):
    shop_index: int
    pet_position: int
