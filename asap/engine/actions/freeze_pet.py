from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionFreezePet(Action):
    shop_index: int
