import pytest

from asap.actions import ActionFreezePet, ActionUnfreezePet, ActionFreezeFood, ActionUnfreezeFood
from asap.engine.action_processor._errors import AlreadyFrozenError, AlreadyUnfrozenError


def test_freeze_unfreeze_pet(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = list(game.team_states.values())[0].shop

    # assert all unfrozen
    assert not any([item.is_frozen() for item in shop.pet_shop._items.values()])
    game.execute_action(ActionFreezePet(0), team)
    # assert first item now frozen
    item = shop.pet_shop.items[0]
    assert item.is_frozen()
    # assert can't re-freeze
    with pytest.raises(AlreadyFrozenError):
        game.execute_action(ActionFreezePet(0), team)
    # assert persistence after shop refresh
    shop.refresh(game.turn)
    assert shop.pet_shop.items[0] == item
    # assert can unfreeze
    game.execute_action(ActionUnfreezePet(0), team)
    # assert first item now frozen
    item = shop.pet_shop.items[0]
    assert not item.is_frozen()
    # assert can't re-unfreeze
    with pytest.raises(AlreadyUnfrozenError):
        game.execute_action(ActionUnfreezePet(0), team)
    # assert non-persistence after shop refresh
    item = shop.pet_shop.items[0]
    shop.refresh(game.turn)
    assert shop.pet_shop.items[0] != item


def test_freeze_food(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = list(game.team_states.values())[0].shop

    # assert all unfrozen
    assert not any([item.is_frozen() for item in shop.food_shop._items.values()])
    game.execute_action(ActionFreezeFood(0), team)
    # assert first item now frozen
    item = shop.food_shop.items[0]
    assert item.is_frozen()
    # assert can't re-freeze
    with pytest.raises(AlreadyFrozenError):
        game.execute_action(ActionFreezeFood(0), team)
    # assert persistence after shop refresh
    shop.refresh(game.turn)
    assert shop.food_shop.items[0] == item
    assert item.is_frozen()
    # assert can unfreeze
    game.execute_action(ActionUnfreezeFood(0), team)
    # assert first item now unfrozen
    item = shop.food_shop.items[0]
    assert not item.is_frozen()
    # assert can't re-unfreeze
    with pytest.raises(AlreadyUnfrozenError):
        game.execute_action(ActionUnfreezeFood(0), team)
    # assert non-persistence after shop refresh
    item = shop.pet_shop.items[0]
    shop.refresh(game.turn)
    assert shop.food_shop.items[0] != item
