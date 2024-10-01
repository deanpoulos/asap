from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionSwapPets(Action):
    position_a: int
    position_b: int
