import random

from asap.abilities import Ability
from asap.pets.pet import Pet


class Beaver(Pet):
    base_attack = 3
    base_health = 2

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = BeaverAbility(self)
        self._perk = None


class BeaverAbility(Ability):
    def on_sell(self, state):
        from asap.team.states import TeamShopState
        state: TeamShopState

        other_pets_in_team = [pet for pet in state.team.pets.values() if pet is not None and pet != self.parent]
        target_pets = random.sample(
            population=other_pets_in_team,
            k=min(2, len(other_pets_in_team))
        )

        for target_pet in target_pets:
            target_pet.extra_attack += self.parent.level
