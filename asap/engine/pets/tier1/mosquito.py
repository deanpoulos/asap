import random
from typing import List

from asap.engine.abilities import Ability
from asap.engine.events.event import Event
from asap.engine.pets.pet import Pet


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
        return self.use_ability(state)

    def use_ability(self, state) -> List[Event]:
        from asap.engine.team.states.battle import TeamBattleState
        state: TeamBattleState

        other_pets = [p for p in state.other_team.pets.values() if p is not None and p.health > 0]
        target_pets = random.sample(
            population=other_pets,
            k=min(self.parent.level, len(other_pets))
        )

        events = []
        for target_pet in target_pets:
            events.extend(target_pet.hurt(1, self, state))

        return events
