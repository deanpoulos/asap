from asap.abilities import Ability
from asap.perks import Perk
from asap.pets.pet import Pet


class Duck(Pet):

    def __init__(self, attack: int = 2, health: int = 3, level: int = 1):
        self._attack = attack
        self._health = health
        self._level = level
        self._ability = DuckAbility()
        self._perk = None

    @property
    def attack(self) -> int:
        return self._attack

    @attack.setter
    def attack(self, value: int):
        self._attack = value

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value

    @property
    def ability(self) -> Ability:
        return self._ability

    @ability.setter
    def ability(self, value: Ability):
        self._ability = value

    @property
    def perk(self) -> Perk:
        return self._perk

    @perk.setter
    def perk(self, value: Perk):
        self._perk = value

    def on_sell(self, state):
        self.ability.on_sell(state)

    def on_buy(self, state):
        self.ability.on_buy(state)


class DuckAbility(Ability):
    def on_sell(self, state):
        from asap.team.states import TeamShopState
        state: TeamShopState

        for pet_item in state.pet_shop.items.values():
            pet_item.pet.health += 1
