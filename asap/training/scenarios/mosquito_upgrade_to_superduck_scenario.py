from asap.engine.engine.game_settings import GameSettings
from asap.engine.pets import Duck, Mosquito, Pet
from asap.engine.shop.settings import SettingsPetShop, SettingsFoodShop

class SuperDuck(Duck):
    base_attack = 10
    base_health = 10

    def __init__(self):
        super().__init__(attack=self.base_attack, health=self.base_health)

mosquito_to_superduck_game_settings = GameSettings(
    num_teams=2,
    starting_team_health=2,
    max_turn=2,
    settings_pet_shop=SettingsPetShop(
        TIER_1_PETS=[Mosquito],
        TIER_2_PETS=[SuperDuck],
        TIER_3_PETS=[Mosquito],
        MAX_ITEMS=5
    ),
    settings_food_shop=SettingsFoodShop(
        MAX_ITEMS=3
    ),
    max_team_size=2
)
