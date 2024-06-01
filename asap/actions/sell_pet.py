from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionSellPet(Action):
    pet_position: int
