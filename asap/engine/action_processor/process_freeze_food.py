from asap.actions import ActionFreezeFood
from asap.actions.errors import *
from asap.team import Team


def process_freeze_food(action: ActionFreezeFood, team: Team, game):
    from asap.engine.game import Game
    game: Game

    shop = game.team_states[team].shop.food_shop
    item = shop.items[action.shop_index]

    if item.is_frozen():
        raise AlreadyFrozenError(item)

    if item.already_bought():
        raise AlreadyBoughtError(item)

    item.freeze()
