from asap.actions import ActionRefreshPetShop
from asap.actions.errors import *
from asap.team import Team


def process_refresh_shop(_: ActionRefreshPetShop, team: Team, game):
    from asap.engine.game import Game
    game: Game

    team_shop_state = game.team_states[team]
    shop = game.team_states[team].pet_shop

    roll_price = shop.roll_price
    if team_shop_state.money < roll_price:
        raise NotEnoughMoneyError(team_shop_state.money, roll_price)

    team_shop_state.money -= roll_price
    shop.refresh(game.turn)
