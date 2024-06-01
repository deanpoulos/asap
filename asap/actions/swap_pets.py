from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionSwapPets(Action):
    position_a: int
    position_b: int
