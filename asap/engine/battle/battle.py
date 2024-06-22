import copy
import random
from typing import Dict, List

from asap.events.event import Event
from asap.pets import Pet
from asap.team.team import Team
from asap.team.states.battle import TeamBattleState


class Battle:
    def __init__(self, team_l: Team, team_r: Team):
        self.team_l = copy.deepcopy(team_l)
        self.team_r = copy.deepcopy(team_r)
        self.team_l_state = TeamBattleState(self.team_l, self.team_r)
        self.team_r_state = TeamBattleState(self.team_r, self.team_l)
        self.event_queue: Dict[Event.Type, Dict[Pet, List[Event]]] = {}
        self.pets_in_priority_order = []

    def play(self):
        while self.teams_are_alive():
            self.attack()

    def teams_are_alive(self):
        return self.team_l_state.team.is_alive() and self.team_r_state.team.is_alive()

    def attack(self):
        self.assign_pet_priorities()
        self.phase_start_of_turn()
        self.phase_before_attack()
        self.phase_trigger_on_hurt_and_faint()
        self.phase_attack()
        self.phase_trigger_on_hurt_and_faint()
        self.phase_after_attack()
        self.phase_trigger_on_hurt_and_faint()
        self.phase_knockout()
        self.phase_trigger_on_hurt_and_faint()

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

    def phase_start_of_turn(self):
        for pet in self.pets_in_priority_order:
            team_state = self._team_state_by_pet(pet)
            events = pet.on_start_battle(team_state)
            self._add_events_to_queue(events)

    def phase_trigger_on_hurt_and_faint(self):
        num_fainted = self._trigger_on_hurt()
        while num_fainted != 0:
            num_fainted = self._trigger_on_hurt()

    def _trigger_on_hurt(self) -> int:
        num_fainted = 0
        # execute on-hurt events for each pet
        for pet in self.pets_in_priority_order:
            team_state = self._team_state_by_pet(pet)
            if Event.Type.HURT in self.event_queue and pet in self.event_queue[Event.Type.HURT]:
                for event in self.event_queue[Event.Type.HURT][pet]:
                    self.execute_event(event)

        # check for faints execute on-faint events for each pet
        for pet in self.pets_in_priority_order:
            if pet.health <= 0:
                num_fainted += 1
                pet.on_faint(team_state)
                team_state.team.remove_pet(pet)

        self.assign_pet_priorities()

        return num_fainted

    def _team_state_by_pet(self, pet: Pet) -> TeamBattleState:
        return self.team_l_state if pet in self.team_l.pets.values() else self.team_r_state

    def _add_events_to_queue(self, events: List[Event]):
        for event in events:
            if event.type in self.event_queue:
                if event.source in self.event_queue[event.type]:
                    self.event_queue[event.type][event.source].append(event)
                else:
                    self.event_queue[event.type][event.source] = [event]
            else:
                self.event_queue[event.type] = {event.source: [event]}

    def _execute_event(self, event: Event):
        event.target.attack += event.delta_attack
        event.target.health += event.delta_health
