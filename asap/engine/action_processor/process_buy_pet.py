from asap.actions import ActionBuyPet
from asap.actions.errors import *
from asap.team import Team


def process_buy_pet(action: ActionBuyPet, team: Team, game):
    from asap.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]
    shop = team_shop_state.pet_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(shop.items[action.shop_index])

    item_price = shop.price(action.shop_index)
    if team_shop_state.money < item_price:
        raise NotEnoughMoneyError(team_shop_state.money, item_price)

    if team.is_full():
        raise TeamFullError()

    if team.pets[action.pet_position] is not None:
        raise PositionOccupiedError(action.pet_position)

    team_shop_state.money -= item_price
    pet = shop.buy(action.shop_index)

    team.pets[action.pet_position] = pet

    pet.on_buy(team_shop_state)
