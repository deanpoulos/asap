from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass(unsafe_hash=True)
class ActionFreezePet(Action):
    shop_index: int
