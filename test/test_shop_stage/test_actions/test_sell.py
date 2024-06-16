import pytest

from asap.actions import ActionSellPet, ActionBuyAndPlacePet
from asap.engine.action_processor._errors import PositionNotOccupiedError
from asap.pets import Duck
from asap.shop.sell import sell_price_pet
from asap.shop.settings import DEFAULT_BUY_PRICE
from asap.engine.game_settings import DEFAULT_STARTING_MONEY as STARTING_MONEY


def test_sell_high_level_pet(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    team_state = game.team_states[team]
    starting_money = team_state.money

    # LVL 1
    team.add_pet(0, Duck(exp=0))
    team.add_pet(1, Duck(exp=1))
    # LVL 2
    team.add_pet(2, Duck(exp=2))
    team.add_pet(3, Duck(exp=3))
    # LVL 3
    team.add_pet(4, Duck(exp=5))

    assert team_state.money == starting_money

    # LVL1 sells for $1
    game.execute_action(ActionSellPet(0), team)
    assert team_state.money == starting_money + 1
    game.execute_action(ActionSellPet(1), team)
    assert team_state.money == starting_money + 1 + 1
    # LVL2 sells for $2
    game.execute_action(ActionSellPet(2), team)
    assert team_state.money == starting_money + 1 + 1 + 2
    game.execute_action(ActionSellPet(3), team)
    assert team_state.money == starting_money + 1 + 1 + 2 + 2
    # LVL 3 sells for $3
    game.execute_action(ActionSellPet(4), team)
    assert team_state.money == starting_money + 1 + 1 + 2 + 2 + 3


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
