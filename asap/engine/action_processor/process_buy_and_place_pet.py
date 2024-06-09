from asap.actions import ActionBuyAndPlacePet
from asap.engine.action_processor.buy_pet import buy_pet
from asap.engine.action_processor._errors import *
from asap.team import Team


def process_buy_and_place_pet(action: ActionBuyAndPlacePet, team: Team, game):
    from asap.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]
    shop = team_shop_state.shop.pet_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(action.shop_index)

    item_price = shop.price(action.shop_index)
    if team_shop_state.money < item_price:
        raise NotEnoughMoneyError(team_shop_state.money, item_price)

    if team.is_full():
        raise TeamFullError()

    if team.pets[action.pet_position] is not None:
        raise PositionOccupiedError(action.pet_position)

    pet = buy_pet(team_shop_state, shop, action)
    team.add_pet(action.pet_position, pet)

    pet.on_buy(team_shop_state)


