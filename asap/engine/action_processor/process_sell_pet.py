from asap.actions import ActionSellPet
from asap.engine.action_processor._errors import *
from asap.shop.sell import sell_price_pet
from asap.team import Team


def process_sell_pet(action: ActionSellPet, team: Team, game):
    from asap.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]
    shop = team_shop_state.shop.pet_shop

    if team.pets[action.pet_position] is None:
        raise PositionNotOccupiedError(action.pet_position)

    pet = team.pets[action.pet_position]
    pet.on_sell(team_shop_state)
    team_shop_state.money += sell_price_pet(pet, shop.settings.PRICE_SELL_PET_BASE)
    team.remove_pet(action.pet_position)
