from abc import ABC, abstractmethod
from asap.perks import Perk
from asap.pets import Pet


class Food(ABC):
    @property
    @abstractmethod
    def attack(self) -> int:
        pass

    @attack.setter
    @abstractmethod
    def attack(self, value: int):
        pass

    @property
    @abstractmethod
    def health(self) -> int:
        pass

    @health.setter
    @abstractmethod
    def health(self, value: int):
        pass

    @property
    @abstractmethod
    def perk(self) -> Perk:
        pass

    @perk.setter
    @abstractmethod
    def perk(self, value: Perk):
        pass

    def on_consume(self, pet: Pet):
        pet.extra_health += self.health
        pet.extra_attack += self.attack
        if self.perk is not None:
            pet.perk = self.perk

    def __str__(self):
        return f"{type(self).__name__}({self.health},{self.attack},{self.perk})"