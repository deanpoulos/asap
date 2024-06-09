from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionUnfreezeFood(Action):
    shop_index: int
