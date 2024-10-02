from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass(unsafe_hash=True)
class ActionSellPet(Action):
    pet_position: int
