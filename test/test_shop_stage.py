import copy

import pytest

from asap.actions.errors import *
from asap.engine.game import Game
from asap.shop.constants import DEFAULT_ROLL_PRICE
from asap.shop.item import DEFAULT_PRICE
from asap.team import Team
from asap.actions import *
from asap.team.states.shop import STARTING_MONEY


def test_freeze_pet():
    team = Team()
    game = Game(teams=[team])
    shop = list(game.team_states.values())[0].shop

    # assert all unfrozen
    assert not any([item.is_frozen() for item in shop.pet_shop.items.values()])
    game.execute_action(ActionFreezePet(0), team)
    # assert first item now frozen
    assert shop.pet_shop.items[0].is_frozen()
    # assert can't re-freeze
    with pytest.raises(AlreadyFrozenError):
        game.execute_action(ActionFreezePet(0), team)


def test_freeze_food():
    team = Team()
    game = Game(teams=[team])
    shop = list(game.team_states.values())[0].shop

    # assert all unfrozen
    assert not any([item.is_frozen() for item in shop.food_shop.items.values()])
    game.execute_action(ActionFreezeFood(0), team)
    # assert first item now frozen
    assert shop.food_shop.items[0].is_frozen()
    # assert can't re-freeze
    with pytest.raises(AlreadyFrozenError):
        game.execute_action(ActionFreezeFood(0), team)


def test_buy_pets_and_refresh():
    team = Team()
    game = Game(teams=[team])
    team_state = game.team_states[team]

    # start with no pets
    assert game.team_states[team].team.pets[0] is None
    # buy a pet
    game.execute_action(ActionBuyPet(0, 0), team)
    # assert team has a pet
    assert game.team_states[team].team.pets[0] is not None
    # assert team paid money
    assert team_state.money == STARTING_MONEY - DEFAULT_PRICE

    # assert can't put another pet on top
    with pytest.raises(PositionOccupiedError):
        game.execute_action(ActionBuyPet(1, 0), team)
    # assert can't re-buy same pet
    with pytest.raises(AlreadyBoughtError):
        game.execute_action(ActionBuyPet(0, 1), team)

    # assert no second pet
    assert game.team_states[team].team.pets[1] is None
    # buy second pet
    game.execute_action(ActionBuyPet(1, 1), team)
    # assert team has second pet
    assert game.team_states[team].team.pets[1] is not None
    # assert team has paid for two pets
    assert team_state.money == STARTING_MONEY - 2*DEFAULT_PRICE

    # buy third pet
    game.execute_action(ActionBuyPet(2, 2), team)
    # assert team has paid for three pets
    assert team_state.money == STARTING_MONEY - 3*DEFAULT_PRICE

    # refresh shop
    game.execute_action(ActionRefreshShop(), team)
    # assert team paid for three pets and shop roll
    assert team_state.money == STARTING_MONEY - 3 * DEFAULT_PRICE - DEFAULT_ROLL_PRICE

    if STARTING_MONEY == 3 * DEFAULT_PRICE + DEFAULT_ROLL_PRICE:
        # assert can't afford pet
        with pytest.raises(NotEnoughMoneyError):
            game.execute_action(ActionBuyPet(0, 0), team)
        # assert can't afford refresh
        with pytest.raises(NotEnoughMoneyError):
            game.execute_action(ActionRefreshShop(), team)


def test_buy_pet_and_food():
    team = Team()
    game = Game(teams=[team])
    team_state = game.team_states[team]

    # buy a pet
    game.execute_action(ActionBuyPet(0, 0), team)
    health, attack = team.pets[0].health, team.pets[0].attack
    # give it food
    game.execute_action(ActionBuyFood(0, 0), team)
    # make sure team has paid
    assert team_state.money == STARTING_MONEY - 2*DEFAULT_PRICE
    assert team.pets[0].health == health + 1
    assert team.pets[0].attack == attack + 1
    # assert its classified as sold
    assert team_state.shop.food_shop.items[0].already_bought()
    # assert it can't be re-bought
    with pytest.raises(AlreadyBoughtError):
        game.execute_action(ActionBuyFood(0, 0), team)

    # refresh shop
    game.execute_action(ActionRefreshShop(), team)
