from asap.foods import Food
from asap.perks import Perk


class Apple(Food):

    def __init__(self, attack: int = 1, health: int = 1):
        self._attack = attack
        self._health = health
        self._perk = None

    @property
    def attack(self) -> int:
        return self._attack

    @attack.setter
    def attack(self, value: int):
        self._attack = value

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value

    @property
    def perk(self) -> Perk:
        return self._perk

    @perk.setter
    def perk(self, value: Perk):
        self._perk = value
