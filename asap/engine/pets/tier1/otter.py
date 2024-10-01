import random

from asap.engine.abilities import Ability
from asap.engine.pets.pet import Pet


class Otter(Pet):
    base_attack = 1
    base_health = 3

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = OtterAbility(self)
        self._perk = None


class OtterAbility(Ability):
    def on_sell(self, state):
        self.use_ability(state)

    def use_ability(self, state):
        from asap.engine.team.states import TeamShopState
        state: TeamShopState

        other_pets_in_team = [pet for pet in state.team.pets.values() if pet is not None and pet != self.parent]
        target_pets = random.sample(
            population=other_pets_in_team,
            k=min(self.parent.level, len(other_pets_in_team))
        )

        for target_pet in target_pets:
            target_pet.extra_health += 1
