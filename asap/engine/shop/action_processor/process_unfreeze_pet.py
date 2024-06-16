from asap.actions import ActionUnfreezePet
from asap.engine.shop.action_processor._errors import *
from asap.team.team import Team


def process_unfreeze_pet(action: ActionUnfreezePet, team: Team, game):
    from asap.engine.game import Game
    game: Game

    shop = game.team_states[team].shop.pet_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(action.shop_index)

    item = shop.items[action.shop_index]

    if not item.is_frozen():
        raise AlreadyUnfrozenError(item)

    item.unfreeze()
