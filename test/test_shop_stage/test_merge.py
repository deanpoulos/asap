import pytest

from asap.actions import ActionMergePets, ActionBuyFood
from asap.engine.action_processor._errors import InvalidMergeError
from asap.foods import Apple
from asap.pets import Duck


def test_merge_high_level_pets_edge_case(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Duck(exp=5))
    team.add_pet(1, Duck(exp=1))

    with pytest.raises(InvalidMergeError):
        game.execute_action(ActionMergePets(1, 0), team)


def test_merge_high_level_pets(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Duck(exp=3))
    team.add_pet(1, Duck(exp=3))

    game.execute_action(ActionMergePets(0, 1), team)

    assert team.pets[1].exp == 5
    assert team.pets[1].level == 3


def test_merge_uneven_extra_stats(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Duck())
    team.add_pet(1, Duck())

    team.pets[0].extra_attack = 3
    team.pets[0].extra_health = 2

    team.pets[1].extra_attack = 1
    team.pets[1].extra_health = 3

    game.execute_action(ActionMergePets(0, 1), team)

    assert team.pets[0] is None
    assert team.pets[1].attack == Duck.base_attack + 3 + 1
    assert team.pets[1].health == Duck.base_health + 3 + 1


def test_merge(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Duck())
    team.add_pet(1, Duck())
    team.add_pet(2, Duck())
    team.add_pet(3, Duck())

    # merge 0 to 1
    with pytest.raises(InvalidMergeError):
        game.execute_action(ActionMergePets(0, -1), team)

    with pytest.raises(InvalidMergeError):
        game.execute_action(ActionMergePets(0, 4), team)

    game.execute_action(ActionMergePets(0, 1), team)

    assert team.pets[0] is None
    assert team.pets[1].exp == 1
    assert team.pets[1].level == 1
    assert team.pets[1].health == Duck.base_health + 1
    assert team.pets[1].attack == Duck.base_attack + 1

    # merge 1 to 2
    with pytest.raises(InvalidMergeError):
        game.execute_action(ActionMergePets(0, 2), team)

    game.execute_action(ActionMergePets(1, 2), team)

    assert team.pets[1] is None
    assert team.pets[2].exp == 2
    assert team.pets[2].level == 2
    assert team.pets[2].health == Duck.base_health + 2
    assert team.pets[2].attack == Duck.base_attack + 2

    # give 3 apple, then merge 2 to 3
    game.execute_action(ActionBuyFood(0, 3), team)
    game.execute_action(ActionMergePets(2, 3), team)

    assert team.pets[2] is None
    assert team.pets[3].exp == 3
    assert team.pets[3].level == 2
    assert team.pets[3].health == Duck.base_health + Apple.base_health + 3
    assert team.pets[3].attack == Duck.base_attack + Apple.base_attack + 3

    # todo: the receiving pet keeps its perk
