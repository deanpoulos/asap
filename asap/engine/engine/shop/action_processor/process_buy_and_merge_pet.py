from asap.engine.actions import ActionBuyAndMergePet
from asap.engine.engine.shop.action_processor.buy_pet import buy_pet
from asap.engine.engine.shop.action_processor._errors import *
from asap.engine.engine.shop.action_processor.merge_pets import merge_pets
from asap.engine.team.team import Team


def process_buy_and_merge_pet(action: ActionBuyAndMergePet, team: Team, game):
    from asap.engine.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]
    shop = team_shop_state.shop.pet_shop

    if shop.already_bought(action.shop_index):
        raise AlreadyBoughtError(action.shop_index)

    item_price = shop.price(action.shop_index)
    if team_shop_state.money < item_price:
        raise NotEnoughMoneyError(team_shop_state.money, item_price)

    if team.pets[action.pet_position] is None:
        raise InvalidBuyMergeError(action.shop_index, action.pet_position)

    if (
        action.pet_position not in team.pets or
        team.pets[action.pet_position] is None or
        not isinstance(shop.items[action.shop_index].item, type(team.pets[action.pet_position])) or
        team.pets[action.pet_position].level == game.settings.max_pet_level
    ):
        raise InvalidBuyMergeError(action.shop_index, action.pet_position)

    giving_pet = buy_pet(team_shop_state, shop, action)
    receiving_pet = team.pets[action.pet_position]

    merge_pets(giving_pet, receiving_pet, team_shop_state)

    receiving_pet.on_buy(team_shop_state)
