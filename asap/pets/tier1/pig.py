from asap.abilities import Ability
from asap.pets.pet import Pet


class Pig(Pet):
    base_attack = 4
    base_health = 1

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = PigAbility(self)
        self._perk = None


class PigAbility(Ability):
    def on_sell(self, state):
        self.use_ability(state)

    def use_ability(self, state):
        from asap.team.states import TeamShopState
        state: TeamShopState

        state.money += self.parent.level
