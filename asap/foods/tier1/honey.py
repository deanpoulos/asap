from asap.foods import Food
from asap.perks import Perk
from asap.pets.tokens.bee import Bee


class Honey(Food):
    base_attack = 0
    base_health = 0

    def __init__(self, attack: int = base_attack, health: int = base_health):
        self._attack = attack
        self._health = health
        self._perk = HoneyPerk()


class HoneyPerk(Perk):
    def on_faint(self, pet_position: int, state):
        from asap.team.states import TeamShopState
        state: TeamShopState

        if not state.team.is_full():
            state.team.push_pet(pet_position, Bee())
