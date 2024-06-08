import pytest

from asap.actions.errors import *
from asap.engine.game import Game
from asap.engine.game_settings import DEFAULT_ROLL_PRICE, GameSettings
from asap.foods import Apple
from asap.pets import Duck
from asap.shop.sell import sell_price_pet
from asap.shop.settings import DEFAULT_BUY_PRICE, SettingsPetShop, SettingsFoodShop
from asap.actions import *
from asap.team.states.shop import STARTING_MONEY


@pytest.fixture()
def game_turn_1_ducks_only_apples_only_single_team():
    settings_pet_shop = SettingsPetShop(TIER_1_PETS=[Duck])
    settings_food_shop = SettingsFoodShop(TIER_1_FOODS=[Apple])

    game_settings = GameSettings(
        settings_pet_shop=settings_pet_shop,
        settings_food_shop=settings_food_shop,
        starting_turn=1
    )
    return Game(num_teams=1, settings=game_settings)


def test_buy_sell_buy_pet(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = game.team_states[team].shop.pet_shop

    # try sell a pet that doesn't exist yet
    with pytest.raises(PositionNotOccupiedError):
        game.execute_action(ActionSellPet(0), team)

    # buy a pet in first position
    game.execute_action(ActionBuyPet(0, 0), team)
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


def test_freeze_pet(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = list(game.team_states.values())[0].shop

    # assert all unfrozen
    assert not any([item.is_frozen() for item in shop.pet_shop.items.values()])
    game.execute_action(ActionFreezePet(0), team)
    # assert first item now frozen
    assert shop.pet_shop.items[0].is_frozen()
    # assert can't re-freeze
    with pytest.raises(AlreadyFrozenError):
        game.execute_action(ActionFreezePet(0), team)


def test_freeze_food(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = list(game.team_states.values())[0].shop

    # assert all unfrozen
    assert not any([item.is_frozen() for item in shop.food_shop.items.values()])
    game.execute_action(ActionFreezeFood(0), team)
    # assert first item now frozen
    assert shop.food_shop.items[0].is_frozen()
    # assert can't re-freeze
    with pytest.raises(AlreadyFrozenError):
        game.execute_action(ActionFreezeFood(0), team)


def test_buy_pets_and_refresh(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    team_state = game.team_states[team]

    # start with no pets
    assert game.team_states[team].team.pets[0] is None
    # buy a pet
    game.execute_action(ActionBuyPet(0, 0), team)
    # assert team has a pet
    assert game.team_states[team].team.pets[0] is not None
    # assert team paid money
    assert team_state.money == STARTING_MONEY - DEFAULT_BUY_PRICE

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
    assert team_state.money == STARTING_MONEY - 2 * DEFAULT_BUY_PRICE

    # buy third pet
    game.execute_action(ActionBuyPet(2, 2), team)
    # assert team has paid for three pets
    assert team_state.money == STARTING_MONEY - 3 * DEFAULT_BUY_PRICE

    # refresh shop
    game.execute_action(ActionRefreshShop(), team)
    # assert team paid for three pets and shop roll
    assert team_state.money == STARTING_MONEY - 3 * DEFAULT_BUY_PRICE - DEFAULT_ROLL_PRICE

    if STARTING_MONEY == 3 * DEFAULT_BUY_PRICE + DEFAULT_ROLL_PRICE:
        # assert can't afford pet
        with pytest.raises(NotEnoughMoneyError):
            game.execute_action(ActionBuyPet(0, 0), team)
        # assert can't afford refresh
        with pytest.raises(NotEnoughMoneyError):
            game.execute_action(ActionRefreshShop(), team)


def test_buy_pet_and_food(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    team_state = game.team_states[team]

    # buy a pet
    game.execute_action(ActionBuyPet(0, 0), team)
    health, attack = team.pets[0].health, team.pets[0].attack
    # give it food
    game.execute_action(ActionBuyFood(0, 0), team)
    # make sure team has paid
    assert team_state.money == STARTING_MONEY - 2 * DEFAULT_BUY_PRICE
    assert team.pets[0].health == health + 1
    assert team.pets[0].attack == attack + 1
    # assert its classified as sold
    assert team_state.shop.food_shop.items[0].already_bought()
    # assert it can't be re-bought
    with pytest.raises(AlreadyBoughtError):
        game.execute_action(ActionBuyFood(0, 0), team)

    # refresh shop
    game.execute_action(ActionRefreshShop(), team)
