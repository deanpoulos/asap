import copy
import random
from collections import defaultdict
from typing import Dict, List

from asap.engine.battle.battle_phase_decorators import updated_priorities, triggers_on_hurt_and_faint
from asap.engine.battle.battle_result import BattleResult, TeamBattleResult
from asap.events.event import *
from asap.pets import Pet
from asap.team.team import Team
from asap.team.states.battle import TeamBattleState


class Battle:
    def __init__(self, team_l: Team, team_r: Team):
        self._team_l = team_l
        self._team_r = team_r
        self.team_l = copy.deepcopy(team_l)
        self.team_r = copy.deepcopy(team_r)
        self.team_l_state = TeamBattleState(self.team_l, self.team_r)
        self.team_r_state = TeamBattleState(self.team_r, self.team_l)
        self.event_queue: Dict[Event.Type, Dict[Pet, List[Event]]] = defaultdict(lambda: defaultdict(list))
        self.pets_in_priority_order = []

    def play(self):
        self.phase_start_of_battle()
        while self._teams_are_alive():
            self.attack()

        return self._get_battle_result()

    def attack(self):
        self.phase_before_attack()
        self.phase_attack()
        self.phase_after_attack()
        self.phase_knockout()

    @updated_priorities
    @triggers_on_hurt_and_faint
    def phase_start_of_battle(self):
        for pet in self.pets_in_priority_order:
            team_state = self._team_state_by_pet(pet)
            events = pet.on_start_battle(team_state)
            self._add_events_to_queue(events)

    @updated_priorities
    @triggers_on_hurt_and_faint
    def phase_before_attack(self):
        for pet in self.pets_in_priority_order:
            if pet in [self.team_l.pets[0], self.team_r.pets[0]]:
                team_state = self._team_state_by_pet(pet)
                events = pet.before_attack(team_state)
                self._add_events_to_queue(events)
            else:
                continue

    @updated_priorities
    def phase_attack(self):
        left_front_pet = self.team_l.pets[0]
        right_front_pet = self.team_r.pets[0]
        # left attacks right
        events = right_front_pet.hurt(left_front_pet.attack, left_front_pet, self.team_r_state)
        self._add_events_to_queue(events)
        # right attacks left
        events = left_front_pet.hurt(right_front_pet.attack, right_front_pet, self.team_l_state)
        self._add_events_to_queue(events)

    @updated_priorities
    @triggers_on_hurt_and_faint
    def phase_after_attack(self):
        for pet in self.pets_in_priority_order:
            if pet in [self.team_l.pets[0], self.team_r.pets[0]]:
                team_state = self._team_state_by_pet(pet)
                events = pet.after_attack(team_state)
                self._add_events_to_queue(events)
            else:
                continue

    @updated_priorities
    @triggers_on_hurt_and_faint
    def phase_knockout(self):
        if KNOCKOUT in self.event_queue:
            while any([len(event_queue) for event_queue in self.event_queue[KNOCKOUT].values()]):
                if KNOCKOUT in self.event_queue:
                    for pet in self.event_queue[KNOCKOUT]:
                        for event in self.event_queue[KNOCKOUT][pet]:
                            event.execute()
                            self.event_queue[KNOCKOUT][pet].remove(event)

    @updated_priorities
    def phase_trigger_on_hurt_and_faint(self):
        num_fainted = self._trigger_on_hurt()
        while num_fainted != 0:
            num_fainted = self._trigger_on_hurt()

    @updated_priorities
    def _trigger_on_hurt(self) -> int:
        num_fainted = 0
        # execute on-hurt events for each pet
        if HURT in self.event_queue:
            for pet in self.pets_in_priority_order:
                if pet in self.event_queue[HURT]:
                    for event in self.event_queue[HURT][pet]:
                        event.execute()
                        self.event_queue[HURT][pet].remove(event)

        # check for faints execute on-faint events for each pet
        for pet in self.pets_in_priority_order:
            if pet.health <= 0:
                num_fainted += 1
                team_state = self._team_state_by_pet(pet)
                pet.on_faint(team_state)

        self._bunch_pets_to_front()

        return num_fainted

    def assign_pet_priorities(self):
        """ Orders pet by current health, then attack. """
        pets_by_attack_and_health = defaultdict(lambda: defaultdict(list))

        # Iterate over both teams' pets
        for pets in [self.team_l.pets.values(), self.team_r.pets.values()]:
            for pet in pets:
                if pet is not None:
                    pets_by_attack_and_health[pet.attack][pet.health].append(pet)

        for attack in pets_by_attack_and_health:
            for health in pets_by_attack_and_health[attack]:
                # for each pet with same attack and health, randomize order
                random.shuffle(pets_by_attack_and_health[attack][health])

        for attack in pets_by_attack_and_health:
            # for each pet with same attack, order by health
            pets_by_attack_and_health[attack] = sum([v for k, v in reversed(sorted(pets_by_attack_and_health[attack].items()))], [])

        # for each pet, order by attack
        self.pets_in_priority_order = sum([v for k, v in reversed(sorted(pets_by_attack_and_health.items()))], [])

    def _bunch_pets_to_front(self):
        for team in [self.team_l, self.team_r]:
            num_pet_slots = len(team.pets)
            pets_list = [pet for pet in team.pets.values() if pet is not None]
            team.pets = {}
            for i in range(0, num_pet_slots):
                if i < len(pets_list):
                    team.pets[i] = pets_list[i]
                else:
                    team.pets[i] = None

    def _team_state_by_pet(self, pet: Pet) -> TeamBattleState:
        return self.team_l_state if pet in self.team_l.pets.values() else self.team_r_state

    def _add_events_to_queue(self, events: List[Event]):
        for event in events:
            self.event_queue[event.type][event.source].append(event)

    def _teams_are_alive(self):
        return self.team_l_state.team.is_alive() and self.team_r_state.team.is_alive()

    def _get_battle_result(self):
        if self.team_l_state.team.is_alive():
            team_l_result = TeamBattleResult.Result.WIN
            team_r_result = TeamBattleResult.Result.LOSS
        elif self.team_r_state.team.is_alive():
            team_l_result = TeamBattleResult.Result.LOSS
            team_r_result = TeamBattleResult.Result.WIN
        else:
            team_l_result = TeamBattleResult.Result.DRAW
            team_r_result = TeamBattleResult.Result.DRAW

        return BattleResult(
            team_l_result=TeamBattleResult(team=self._team_l, result=team_l_result),
            team_r_result=TeamBattleResult(team=self._team_r, result=team_r_result)
        )
