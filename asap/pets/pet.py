from asap.abilities import Ability
from asap.perks import Perk


class Pet:
    def __init__(self):
        self._extra_attack = 0
        self._extra_health = 0

    @property
    def extra_attack(self) -> int:
        return self._extra_attack

    @extra_attack.setter
    def extra_attack(self, value: int):
        self._extra_attack = value

    @property
    def attack(self) -> int:
        return (self._attack +
                self._extra_attack +
                self._exp)

    @property
    def extra_health(self) -> int:
        return self._extra_health

    @extra_health.setter
    def extra_health(self, value: int):
        self._extra_health = value

    @property
    def health(self) -> int:
        return (self._health +
                self._extra_health +
                self._exp)

    @property
    def ability(self) -> Ability:
        return self._ability

    @ability.setter
    def ability(self, value: Ability):
        self._ability = value

    @property
    def perk(self) -> Perk:
        return self._perk

    @perk.setter
    def perk(self, value: Perk):
        self._perk = value

    def on_sell(self, state):
        self.ability.on_sell(state)

    def on_buy(self, state):
        self.ability.on_buy(state)

    def add_1_exp(self):
        if self._exp < 5:
            self._exp += 1
        else:
            raise Exception()

    @property
    def exp(self) -> int:
        return self._exp

    @property
    def level(self) -> int:
        if self._exp < 2:
            return 1
        elif self._exp < 5:
            return 2
        else:
            return 3

    def __str__(self):
        return f"{type(self).__name__}({self.attack},{self.health})"
