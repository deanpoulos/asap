from asap.abilities import Ability
from asap.engine.subscribers.pet_subscriber import PetSubscriber
from asap.perks import Perk


LEVEL_2_EXP = 2
LEVEL_3_EXP = 5
MAX_HEALTH = 50
MAX_ATTACK = 50


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
        value = min(value, MAX_ATTACK - self.attack)
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
        value = min(value, MAX_HEALTH - self.attack)
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

    def add_exp(self, value: int, state):
        if self.exp == LEVEL_3_EXP:
            raise Exception()
        dont_trigger_on_level = False
        if self.level == 2 and value >= LEVEL_2_EXP:
            # no rewards for merging two level 2 pets
            dont_trigger_on_level = True
        for _ in range(min(value, LEVEL_3_EXP - self._exp)):
            self._add_one_exp(state, dont_trigger_on_level)

    def _add_one_exp(self, state, dont_trigger_on_level: bool):
        if self._exp < LEVEL_3_EXP:
            about_to_level_up = self._exp in [LEVEL_2_EXP-1, LEVEL_3_EXP-1]
            if about_to_level_up and not dont_trigger_on_level:
                self.ability.on_level(state)
                if self._subscriber is not None:
                    self._subscriber.notify_level_change()
            self._exp += 1
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
