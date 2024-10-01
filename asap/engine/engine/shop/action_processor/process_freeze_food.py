from asap.engine.actions import ActionFreezeFood
from asap.engine.engine.shop.action_processor._errors import *
from asap.engine.team.team import Team


def process_freeze_food(action: ActionFreezeFood, team: Team, game):
    from asap.engine.engine.game import Game
    game: Game

    shop = game.team_states[team].shop.food_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(action.shop_index)

    item = shop.items[action.shop_index]

    if item.is_frozen():
        raise AlreadyFrozenError(item)

    item.freeze()
