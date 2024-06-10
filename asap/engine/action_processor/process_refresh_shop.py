from asap.actions import ActionRefreshShop
from asap.engine.action_processor._errors import *
from asap.engine.action_validator.validate_refresh_shop import validate_refresh_shop
from asap.team import Team


def process_refresh_shop(_: ActionRefreshShop, team: Team, game):
    from asap.engine.game import Game
    game: Game

    team_shop_state = game.team_states[team]
    shop = game.team_states[team].shop

    roll_price = shop.roll_price
    if not validate_refresh_shop(team_shop_state):
        raise NotEnoughMoneyError(team_shop_state.money, roll_price)

    team_shop_state.money -= roll_price
    shop.refresh()
