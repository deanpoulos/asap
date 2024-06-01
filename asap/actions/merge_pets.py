from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionMergePet(Action):
    position_a: int
    position_b: int
