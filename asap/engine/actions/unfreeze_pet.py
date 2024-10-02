from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass(unsafe_hash=True)
class ActionUnfreezePet(Action):
    shop_index: int
