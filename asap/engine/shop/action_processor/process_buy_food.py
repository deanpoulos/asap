from asap.actions import ActionBuyFood
from asap.engine.shop.action_processor._errors import *
from asap.team.team import Team


def process_buy_food(action: ActionBuyFood, team: Team, game):
    from asap.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]
    shop = team_shop_state.shop.food_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(action.shop_index)

    item_price = shop.price(action.shop_index)
    if team_shop_state.money < item_price:
        raise NotEnoughMoneyError(team_shop_state.money, item_price)

    pet = team.pets[action.pet_position]
    if pet is None:
        raise PositionNotOccupiedError(action.pet_position)

    team_shop_state.money -= item_price
    food = team_shop_state.shop.buy_food(action.shop_index)

    food.on_consume(pet)
