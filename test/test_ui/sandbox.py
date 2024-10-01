from asap.engine.engine.game import Game
from asap.engine.engine.game_settings import GameSettings
from asap.engine.pets import Duck
from asap.engine.shop.settings import SettingsPetShop
from asap.engine.ui.game_ui import GameUI


def test_sandbox():
    settings_pet_shop = SettingsPetShop(TIER_2_PETS=[Duck])
    settings = GameSettings(num_teams=1, starting_money=10, settings_pet_shop=settings_pet_shop)
    game = Game(settings=settings)

    app = GameUI(game)
    app.mainloop()
