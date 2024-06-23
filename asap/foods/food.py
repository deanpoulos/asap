from abc import ABC, abstractmethod
from asap.perks import Perk
from asap.pets import Pet


class Food(ABC):
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

    def on_consume(self, pet: Pet):
        pet.extra_health += self.health
        pet.extra_attack += self.attack
        if self.perk is not None:
            pet.perk = self.perk

    def __str__(self):
        return f"{type(self).__name__}({self.health},{self.attack},{self.perk})"