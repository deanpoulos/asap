from typing import List

from asap.engine.events.event import Event


class AbilityBase:
    def use_ability(self, state):
        pass

    def on_start_of_battle(self, state) -> List[Event]:
        return []

    def on_end_turn(self, state):
        pass

    def on_buy(self, state):
        pass

    def on_sell(self, state):
        pass

    def on_friend_summoned(self, friend):
        pass

    def on_level(self, state):
        pass

    def on_faint(self, pet_position: int, state):
        pass

    def on_hurt(self, source, state) -> List[Event]:
        return []

    def before_attack(self, state) -> List[Event]:
        return []

    def after_attack(self, state) -> List[Event]:
        return []


class Ability(AbilityBase):
    def __init__(self, parent: 'Pet'):
        self.parent = parent
        pass

