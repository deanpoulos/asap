from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionFreezeFood(Action):
    shop_index: int
