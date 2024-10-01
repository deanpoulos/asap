from dataclasses import dataclass

from asap.engine.actions import Action


@dataclass
class ActionUnfreezePet(Action):
    shop_index: int
