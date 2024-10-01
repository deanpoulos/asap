import pytest

from asap.engine.actions import ActionBuyAndMergePet
from asap.engine.engine.shop.action_processor._errors import InvalidBuyMergeError
from asap.engine.pets import Duck


def test_buy_and_merge(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Duck())

    # merge shop 0 to 0
    with pytest.raises(InvalidBuyMergeError):
        game.execute_action(ActionBuyAndMergePet(0, 1), team)

    game.execute_action(ActionBuyAndMergePet(0, 0), team)

    assert team.pets[0].exp == 1
    assert team.pets[0].level == 1
    assert team.pets[0].health == Duck.base_health + 1
    assert team.pets[0].attack == Duck.base_attack + 1

    shop = game.team_states[team].shop
    game.team_states[team].money = 100
    for _ in range(4):
        shop.refresh()
        game.execute_action(ActionBuyAndMergePet(0, 0), team)

    assert team.pets[0].exp == 5
    assert team.pets[0].level == 3
    assert team.pets[0].health == Duck.base_health + 5
    assert team.pets[0].attack == Duck.base_attack + 5

    # assert can't merge beyond max level
    shop.refresh()
    with pytest.raises(InvalidBuyMergeError):
        game.execute_action(ActionBuyAndMergePet(0, 0), team)
