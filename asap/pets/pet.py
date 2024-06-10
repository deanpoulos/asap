from asap.abilities import Ability
from asap.engine.subscribers.pet_subscriber import PetSubscriber
from asap.perks import Perk


LEVEL_2_EXP = 2
LEVEL_3_EXP = 5

class Pet:
    def __init__(self):
        self._extra_attack = 0
        self._extra_health = 0
        self._subscriber = None

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

    def add_subscriber(self, subscriber: PetSubscriber):
        self._subscriber = subscriber

    def add_1_exp(self):
        if self._exp < LEVEL_3_EXP:
            self._exp += 1
            if (self._subscriber is not None and
                self._exp in [LEVEL_2_EXP, LEVEL_3_EXP]):
                self._subscriber.notify_level_change()
        else:
            raise Exception()

    @property
    def exp(self) -> int:
        return self._exp

    @property
    def level(self) -> int:
        if self._exp < LEVEL_2_EXP:
            return 1
        elif self._exp < LEVEL_3_EXP:
            return 2
        else:
            return 3

    def __str__(self):
        return f"{type(self).__name__}({self.attack},{self.health})"
