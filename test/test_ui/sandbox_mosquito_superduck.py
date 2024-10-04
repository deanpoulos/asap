from asap.engine.engine.game import Game
from asap.engine.engine.game_settings import GameSettings
from asap.engine.pets import Duck, Mosquito
from asap.engine.shop.settings import SettingsPetShop, SettingsFoodShop
from asap.engine.ui.game_ui import GameUI


def test_sandbox():
    class Fish(Duck):
        base_attack = 10
        base_health = 10

        def __init__(self):
            super().__init__(attack=self.base_attack, health=self.base_health)

    settings = GameSettings(
        num_teams=2,
        starting_team_health=2,
        max_turn=2,
        settings_pet_shop=SettingsPetShop(
            TIER_1_PETS=[Mosquito],
            TIER_2_PETS=[Fish],
            TIER_3_PETS=[Mosquito],
            MAX_ITEMS=5
        ),
        settings_food_shop=SettingsFoodShop(
            MAX_ITEMS=3
        ),
        max_team_size=2
    )

    game = Game(settings=settings)

    app = GameUI(game)
    app.mainloop()
