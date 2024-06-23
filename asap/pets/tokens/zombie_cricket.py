from asap.abilities import Ability
from asap.abilities.null_ability import NullAbility
from asap.pets.pet import Pet


class ZombieCricket(Pet):
    base_attack = 1
    base_health = 1

    def __init__(self, cricket_level: int):
        super().__init__()
        self._attack = self.base_attack * cricket_level
        self._health = self.base_attack * cricket_level
        self._exp = 0
        self._ability = NullAbility(self)
        self._perk = None
