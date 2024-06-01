from abc import ABC, abstractmethod
from asap.engine.abilities import Ability
from asap.engine.food import Perk


class Pet(ABC):

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
    def level(self) -> int:
        pass

    @level.setter
    @abstractmethod
    def level(self, value: int):
        pass

    @property
    @abstractmethod
    def ability(self) -> Ability:
        pass

    @ability.setter
    @abstractmethod
    def ability(self, value: Ability):
        pass

    @property
    @abstractmethod
    def perk(self) -> Perk:
        pass

    @perk.setter
    @abstractmethod
    def perk(self, value: Perk):
        pass

    @abstractmethod
    def on_sell(self, state):
        pass

    @abstractmethod
    def on_buy(self, state):
        pass

    def __str__(self):
        return f"{type(self).__name__}({self.health},{self.attack})"