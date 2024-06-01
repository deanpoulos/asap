from asap.actions import ActionRefreshShop
from asap.actions.errors import *
from asap.team import Team


def process_refresh_shop(_: ActionRefreshShop, team: Team, game):
    from asap.engine.game import Game
    game: Game

    team_shop_state = game.team_states[team]
    pet_shop = game.team_states[team].pet_shop
    food_shop = game.team_states[team].food_shop

    roll_price = pet_shop.roll_price
    if team_shop_state.money < roll_price:
        raise NotEnoughMoneyError(team_shop_state.money, roll_price)

    team_shop_state.money -= roll_price
    pet_shop.refresh(game.turn)
    food_shop.refresh(game.turn)
