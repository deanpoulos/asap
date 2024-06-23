import random
from typing import List

from asap.abilities import Ability
from asap.events.event import Event
from asap.pets.pet import Pet


class Ant(Pet):
    base_attack = 2
    base_health = 2

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = AntAbility(self)
        self._perk = None


class AntAbility(Ability):
    def on_faint(self, pet_position: int, state):
        from asap.team.states.battle import TeamBattleState
        state: TeamBattleState

        other_pets = [p for p in state.team.pets.values() if p != state.team.pets[pet_position]]
        other_living_pets = [p for p in other_pets if p is not None and p.health > 0]
        target_pets = random.sample(
            population=other_living_pets,
            k=min(1, len(other_living_pets))
        )

        for target_pet in target_pets:
            target_pet.extra_health += self.parent.level
            target_pet.extra_attack += self.parent.level

        return []
