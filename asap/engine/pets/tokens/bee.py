from asap.engine.abilities import Ability
from asap.engine.abilities.null_ability import NullAbility
from asap.engine.pets.pet import Pet


class Bee(Pet):
    base_attack = 1
    base_health = 1

    def __init__(self):
        super().__init__()
        self._attack = self.base_attack
        self._health = self.base_attack
        self._exp = 0
        self._ability = NullAbility(self)
        self._perk = None

