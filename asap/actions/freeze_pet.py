from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionFreezePet(Action):
    shop_index: int
