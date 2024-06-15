from asap.actions import *
from asap.pets import Duck


def test_refresh(game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy, DummyTier2Pet):
    game = game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy
    team = game.teams[0]
    shop = game.team_states[team].shop

    shop_items = list(shop.pet_shop._items.values())

    # assert no items persist if not frozen
    shop.refresh()
    new_shop_items = list(shop.pet_shop._items.values())
    for new_shop_item in new_shop_items:
        assert new_shop_item not in shop_items

    # assert all items that are frozen persist
    for new_shop_item in new_shop_items:
        new_shop_item.freeze()
    shop.refresh()
    new_new_shop_items = list(shop.pet_shop._items.values())
    for i in range(3):
        assert new_shop_items[i] == new_new_shop_items[i]


def test_merge_level_up_generates_higher_tier_pet_shop_options(game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy, DummyTier2Pet):
    game = game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy
    team = game.teams[0]
    shop = game.team_states[team].shop
    game.team_states[team].money = 100

    game.execute_action(ActionBuyAndPlacePet(0, 0), team)

    # no new options on single merge
    game.execute_action(ActionBuyAndMergePet(1, 0), team)
    assert len(shop.pet_shop._items) == 3

    # assert next highest tier pets are made available
    game.execute_action(ActionRefreshShop(), team)
    game.execute_action(ActionBuyAndMergePet(2, 0), team)
    assert len(shop.pet_shop._items) == 5
    assert isinstance(shop.pet_shop._items[0].item, DummyTier2Pet)
    assert isinstance(shop.pet_shop._items[1].item, DummyTier2Pet)

    # assert next highest tier pets persist if frozen
    game.execute_action(ActionFreezePet(0), team)
    game.execute_action(ActionFreezePet(1), team)
    game.execute_action(ActionFreezePet(2), team)
    game.execute_action(ActionFreezePet(3), team)
    game.execute_action(ActionRefreshShop(), team)
    assert isinstance(shop.pet_shop._items[0].item, DummyTier2Pet)
    assert isinstance(shop.pet_shop._items[1].item, DummyTier2Pet)

    # assert frozen items can exceed max shop size
    assert len(shop.pet_shop._items) == 4


def test_merge_level_up_generates_higher_tier_pet_shop_options_edge_case(game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy, DummyTier2Pet):
    game = game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy
    team = game.teams[0]
    shop = game.team_states[team].shop
    game.team_states[team].money = 100

    game.execute_action(ActionBuyAndPlacePet(0, 0), team)
    game.execute_action(ActionBuyAndPlacePet(1, 1), team)
    game.execute_action(ActionBuyAndPlacePet(2, 2), team)
    game.execute_action(ActionMergePets(2, 1), team)
    game.execute_action(ActionMergePets(1, 0), team)

    # assert next highest tier pets are made available
    assert len(shop.pet_shop.items) == 2
    assert isinstance(shop.pet_shop.items[0].item, DummyTier2Pet)
    assert isinstance(shop.pet_shop.items[1].item, DummyTier2Pet)
