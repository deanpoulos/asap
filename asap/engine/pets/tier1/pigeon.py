from asap.engine.abilities import Ability
from asap.engine.pets.pet import Pet


class Pigeon(Pet):
    base_attack = 3
    base_health = 1

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = PigeonAbility(self)
        self._perk = None


class PigeonAbility(Ability):
    def on_sell(self, state):
        self.use_ability(state)

    def use_ability(self, state):
        from asap.engine.foods.tokens.bread_crumbs import BreadCrumbs
        from asap.engine.shop.item import FoodItem
        from asap.engine.team.states import TeamShopState
        state: TeamShopState

        foods = [FoodItem(BreadCrumbs(), price=0) for _ in range(self.parent.level)]
        state.shop.stock_special_foods(foods)
