import random

from asap.abilities import Ability
from asap.pets.pet import Pet


class Mosquito(Pet):
    base_attack = 2
    base_health = 2

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = MosquitoAbility(self)
        self._perk = None


class MosquitoAbility(Ability):
    def on_start_of_battle(self, state):
        self.use_ability(state)

    def use_ability(self, state):
        from asap.team.states.battle import TeamBattleState
        state: TeamBattleState

        other_pets = [p for p in state.other_team.pets.values() if p is not None and p.health > 0]
        target_pets = random.sample(
            population=other_pets,
            k=min(self.parent.level, len(other_pets))
        )

        for target_pet in target_pets:
            target_pet.hurt(1, state)
