from asap.actions import ActionBuyFood
from asap.actions.errors import *
from asap.team import Team


def process_buy_food(action: ActionBuyFood, team: Team, game):
    from asap.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]
    shop = team_shop_state.shop.food_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(shop.items[action.shop_index])

    item_price = shop.price(action.shop_index)
    if team_shop_state.money < item_price:
        raise NotEnoughMoneyError(team_shop_state.money, item_price)

    pet = team.pets[action.pet_position]
    if pet is None:
        raise PositionNotOccupiedError(action.pet_position)

    team_shop_state.money -= item_price
    food = shop.buy(action.shop_index)

    food.on_consume(pet)
