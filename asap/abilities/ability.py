

class Ability:
    def __init__(self, parent: 'Pet'):
        self.parent = parent
        pass

    def on_start_of_battle(self):
        pass

    def on_end_turn(self, state):
        pass

    def on_buy(self, state):
        pass

    def on_sell(self, state):
        pass

    def on_level(self, state):
        pass

    def on_faint(self):
        pass

    def on_hurt(self):
        pass
