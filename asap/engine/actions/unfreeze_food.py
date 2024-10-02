from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass(unsafe_hash=True)
class ActionUnfreezeFood(Action):
    shop_index: int
