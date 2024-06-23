from asap.abilities import Ability
from asap.pets.pet import Pet
from asap.pets.tokens.zombie_cricket import ZombieCricket


class Cricket(Pet):
    base_attack = 1
    base_health = 2

    def __init__(self, attack: int = base_attack, health: int = base_health, exp: int = 0):
        super().__init__()
        self._attack = attack
        self._health = health
        self._exp = exp
        self._ability = DuckAbility(self)
        self._perk = None


class DuckAbility(Ability):
    def on_faint(self, pet_position, state):
        from asap.team.states import TeamShopState
        state: TeamShopState

        if not state.team.is_full():
            state.team.push_pet(pet_position, ZombieCricket(self.parent.level))
