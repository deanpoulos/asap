import copy
import random

from asap.pets import Pet
from asap.team.team import Team
from asap.team.states.battle import TeamBattleState


class Battle:
    def __init__(self, team_l: Team, team_r: Team):
        self.team_l = copy.deepcopy(team_l)
        self.team_r = copy.deepcopy(team_r)
        self.team_l_state = TeamBattleState(self.team_l, self.team_r)
        self.team_r_state = TeamBattleState(self.team_r, self.team_l)
        self.pets_in_priority_order = []

    def play(self):
        self.assign_pet_priorities()
        self.start_of_turn()
        self.trigger_on_hurt()

    def assign_pet_priorities(self):
        pets_by_attack_and_health = {}
        for pets in [self.team_l.pets.values(), self.team_r.pets.values()]:
            for pet in pets:
                if pet is not None:
                    if pet.attack in pets_by_attack_and_health:
                        if pet.health in pets_by_attack_and_health[pet.attack]:
                            pets_by_attack_and_health[pet.attack][pet.health].append(pet)
                        else:
                            pets_by_attack_and_health[pet.attack][pet.health] = [pet]
                    else:
                        pets_by_attack_and_health[pet.attack] = {pet.health: [pet]}

        for attack in pets_by_attack_and_health:
            for health in pets_by_attack_and_health[attack]:
                # for each pet with same attack and health, randomize order
                random.shuffle(pets_by_attack_and_health[attack][health])

        for attack in pets_by_attack_and_health:
            # for each pet with same attack, order by health
            pets_by_attack_and_health[attack] = sum([v for k, v in reversed(sorted(pets_by_attack_and_health[attack].items()))], [])

        # for each pet, order by attack
        self.pets_in_priority_order = sum([v for k, v in reversed(sorted(pets_by_attack_and_health.items()))], [])

    def start_of_turn(self):
        for pet in self.pets_in_priority_order:
            team_state = self._team_state_by_pet(pet)
            pet.on_start_battle(team_state)

    def trigger_on_hurt(self):
        num_fainted = self._trigger_on_hurt()
        while num_fainted != 0:
            num_fainted = self._trigger_on_hurt()

    def _trigger_on_hurt(self) -> int:
        num_fainted = 0
        for pet in self.pets_in_priority_order:
            team_state = self._team_state_by_pet(pet)
            pet.trigger_delayed_event(pet.on_hurt, team_state)
            if pet.health <= 0:
                num_fainted += 1
                pet.on_faint(team_state)
                team_state.team.remove_pet(pet)
        self.assign_pet_priorities()

        return num_fainted

    def _team_state_by_pet(self, pet: Pet) -> TeamBattleState:
        return self.team_l_state if pet in self.team_l.pets.values() else self.team_r_state
