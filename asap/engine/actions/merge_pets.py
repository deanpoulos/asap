from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass(unsafe_hash=True)
class ActionMergePets(Action):
    position_from: int
    position_to: int
