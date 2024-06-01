from asap.actions import ActionFreezePet
from asap.actions.errors import *
from asap.team import Team


def process_freeze_pet(action: ActionFreezePet, team: Team, game):
    from asap.engine.game import Game
    game: Game

    shop = game.team_states[team].pet_shop
    item = shop.items[action.shop_index]

    if item.is_frozen():
        raise AlreadyFrozenError(item)

    if item.already_bought():
        raise AlreadyBoughtError(item)

    item.freeze()
