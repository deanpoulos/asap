from asap.engine.game import Game
from asap.engine.game_settings import GameSettings
from asap.pets import Duck
from asap.shop.settings import SettingsPetShop
from asap.ui.game_ui import GameUI


def test_sandbox():
    settings_pet_shop = SettingsPetShop(TIER_2_PETS=[Duck])
    settings = GameSettings(starting_money=10, settings_pet_shop=settings_pet_shop)
    game = Game(num_teams=1, settings=settings)

    app = GameUI(game)
    app.mainloop()
