import random

from asap.abilities import Ability
from asap.pets.pet import Pet


class Horse(Pet):
    base_attack = 2
    base_health = 1

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = HorseAbility(self)
        self._perk = None


class HorseAbility(Ability):
    def on_friend_summoned(self, friend: Pet):
        self.use_ability(friend)

    def use_ability(self, friend: Pet):
        friend.temp_attack += self.parent.level
