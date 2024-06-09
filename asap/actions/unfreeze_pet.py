from dataclasses import dataclass

from asap.actions import Action


@dataclass
class ActionUnfreezePet(Action):
    shop_index: int
