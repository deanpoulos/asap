from asap.abilities import Ability
from asap.pets.pet import Pet


class Duck(Pet):
    base_attack = 2
    base_health = 3

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = DuckAbility(self)
        self._perk = None


class DuckAbility(Ability):
    def on_sell(self, state):
        self.use_ability(state)

    def use_ability(self, state):
        from asap.team.states import TeamShopState
        state: TeamShopState

        for pet_item in state.shop.pet_shop.items.values():
            pet_item.item.extra_health += self.parent.level
