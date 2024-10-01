from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionMergePets(Action):
    position_from: int
    position_to: int
