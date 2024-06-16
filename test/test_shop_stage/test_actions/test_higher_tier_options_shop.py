from asap.actions import ActionMergePets, ActionBuyAndPlacePet, ActionFreezePet, ActionRefreshShop
from asap.pets import Duck


def test_paired_higher_tier_shop_items_after_freezing(game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy):
    game = game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy
    team = game.teams[0]
    game.team_states[team].money = 100

    game.execute_action(ActionBuyAndPlacePet(0, 0), team)
    game.execute_action(ActionBuyAndPlacePet(1, 1), team)
    game.execute_action(ActionBuyAndPlacePet(2, 2), team)

    game.execute_action(ActionMergePets(2, 0), team)
    game.execute_action(ActionMergePets(1, 0), team)

    # Get access to higher tier pets
    assert len(game.team_states[team].shop.pet_shop.items) == 2

    # Freeze both higher tier pet options
    game.execute_action(ActionFreezePet(0), team)
    game.execute_action(ActionFreezePet(1), team)

    # Refresh the shop
    game.execute_action(ActionRefreshShop(), team)

    # Assume they persists- first two are higher tier, last is not
    assert len(game.team_states[team].shop.pet_shop.items) == 3

    # Buy the second of the higher tier options
    game.execute_action(ActionBuyAndPlacePet(1, 1), team)

    # Can only buy one of the higher tier pet options, after which the other disappears
    assert len(game.team_states[team].shop.pet_shop.items) == 1


def test_paired_higher_tier_shop_items(game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy):
    game = game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy
    team = game.teams[0]
    game.team_states[team].money = 100

    game.execute_action(ActionBuyAndPlacePet(0, 0), team)
    game.execute_action(ActionBuyAndPlacePet(1, 1), team)
    game.execute_action(ActionBuyAndPlacePet(2, 2), team)

    game.execute_action(ActionMergePets(2, 0), team)
    game.execute_action(ActionMergePets(1, 0), team)

    assert len(game.team_states[team].shop.pet_shop.items) == 2

    game.execute_action(ActionBuyAndPlacePet(0, 1), team)

    # Can only buy one of the higher tier pet options, after which the other disappears
    assert len(game.team_states[team].shop.pet_shop.items) == 0


def test_no_shop_rewards_on_combining_level_2s(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Duck(exp=2))
    team.add_pet(1, Duck(exp=2))

    game.execute_action(ActionMergePets(1, 0), team)

    assert len(game.team_states[team].shop.pet_shop.items) == 3


