from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionSellPet(Action):
    pet_position: int
