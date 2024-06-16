import pytest

from asap.actions import ActionBuyAndPlacePet, ActionRefreshShop, ActionBuyFood
from asap.engine.action_processor._errors import PositionOccupiedError, AlreadyBoughtError, NotEnoughMoneyError
from asap.engine.game_settings import DEFAULT_ROLL_PRICE
from asap.shop.settings import DEFAULT_BUY_PRICE
from asap.engine.game_settings import DEFAULT_STARTING_MONEY as STARTING_MONEY


def test_buy_pets_and_refresh(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    team_state = game.team_states[team]

    # start with no pets
    assert game.team_states[team].team.pets[0] is None
    # buy a pet
    game.execute_action(ActionBuyAndPlacePet(0, 0), team)
    # assert team has a pet
    assert game.team_states[team].team.pets[0] is not None
    # assert team paid money
    assert team_state.money == STARTING_MONEY - DEFAULT_BUY_PRICE

    # assert can't put another pet on top
    with pytest.raises(PositionOccupiedError):
        game.execute_action(ActionBuyAndPlacePet(1, 0), team)
    # assert can't re-buy same pet
    with pytest.raises(AlreadyBoughtError):
        game.execute_action(ActionBuyAndPlacePet(0, 1), team)

    # assert no second pet
    assert game.team_states[team].team.pets[1] is None
    # buy second pet
    game.execute_action(ActionBuyAndPlacePet(1, 1), team)
    # assert team has second pet
    assert game.team_states[team].team.pets[1] is not None
    # assert team has paid for two pets
    assert team_state.money == STARTING_MONEY - 2 * DEFAULT_BUY_PRICE

    # buy third pet
    game.execute_action(ActionBuyAndPlacePet(2, 2), team)
    # assert team has paid for three pets
    assert team_state.money == STARTING_MONEY - 3 * DEFAULT_BUY_PRICE

    # refresh shop
    game.execute_action(ActionRefreshShop(), team)
    # assert team paid for three pets and shop roll
    assert team_state.money == STARTING_MONEY - 3 * DEFAULT_BUY_PRICE - DEFAULT_ROLL_PRICE

    if STARTING_MONEY == 3 * DEFAULT_BUY_PRICE + DEFAULT_ROLL_PRICE:
        # assert can't afford pet
        with pytest.raises(NotEnoughMoneyError):
            game.execute_action(ActionBuyAndPlacePet(0, 0), team)
        # assert can't afford refresh
        with pytest.raises(NotEnoughMoneyError):
            game.execute_action(ActionRefreshShop(), team)


def test_buy_pet_and_food(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    team_state = game.team_states[team]

    # buy a pet
    game.execute_action(ActionBuyAndPlacePet(0, 0), team)
    health, attack = team.pets[0].health, team.pets[0].attack
    # give it food
    game.execute_action(ActionBuyFood(0, 0), team)
    # make sure team has paid
    assert team_state.money == STARTING_MONEY - 2 * DEFAULT_BUY_PRICE
    assert team.pets[0].health == health + 1
    assert team.pets[0].attack == attack + 1

    # assert it can't be re-bought
    with pytest.raises(AlreadyBoughtError):
        game.execute_action(ActionBuyFood(0, 0), team)

    # refresh shop
    game.execute_action(ActionRefreshShop(), team)
