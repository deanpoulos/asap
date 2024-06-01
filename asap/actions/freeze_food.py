from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionFreezeFood(Action):
    shop_index: int
