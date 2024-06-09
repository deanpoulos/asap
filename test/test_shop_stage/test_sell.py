import pytest

from asap.actions import ActionSellPet, ActionBuyAndPlacePet
from asap.engine.action_processor._errors import PositionNotOccupiedError
from asap.shop.sell import sell_price_pet
from asap.shop.settings import DEFAULT_BUY_PRICE
from asap.team.states.shop import STARTING_MONEY


def test_buy_sell_buy_pet(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = game.team_states[team].shop.pet_shop

    # try sell a pet that doesn't exist yet
    with pytest.raises(PositionNotOccupiedError):
        game.execute_action(ActionSellPet(0), team)

    # buy a pet in first position
    game.execute_action(ActionBuyAndPlacePet(0, 0), team)
    pet = team.pets[0]

    # try sell a pet in a different position
    with pytest.raises(PositionNotOccupiedError):
        game.execute_action(ActionSellPet(1), team)

    # sell the pet in the correct position
    game.execute_action(ActionSellPet(0), team)
    assert game.team_states[team].money == (
            STARTING_MONEY -
            DEFAULT_BUY_PRICE +
            sell_price_pet(pet, shop.settings.PRICE_SELL_PET_BASE)
    )
