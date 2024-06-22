from typing import List

from asap.events.event import Event


class Ability:
    def __init__(self, parent: 'Pet'):
        self.parent = parent
        pass

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

    def on_faint(self, state):
        pass

    def on_hurt(self, state) -> List[Event]:
        return []
