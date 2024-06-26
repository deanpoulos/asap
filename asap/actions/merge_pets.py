from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionMergePets(Action):
    position_from: int
    position_to: int
