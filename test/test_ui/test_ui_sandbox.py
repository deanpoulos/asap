from asap.engine.game import Game
from asap.engine.game_settings import GameSettings
from asap.pets import Duck
from asap.shop.settings import SettingsPetShop
from asap.ui.game_ui import GameUI

def test_sandbox():
    settings = GameSettings(starting_money=100,
                            settings_pet_shop=SettingsPetShop(
                                TIER_2_PETS=[Duck]
                            ))
    game = Game(num_teams=1, settings=settings)

    app = GameUI(game)
    app.mainloop()
