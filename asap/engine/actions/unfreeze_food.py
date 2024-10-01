from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionUnfreezeFood(Action):
    shop_index: int
