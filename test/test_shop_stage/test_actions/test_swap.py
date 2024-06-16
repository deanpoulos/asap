import pytest

from asap.actions import ActionSwapPets
from asap.engine.shop.action_processor._errors import InvalidSwapError
from asap.pets import Duck


def test_swap_pets(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    with pytest.raises(InvalidSwapError):
        game.execute_action(ActionSwapPets(0, 0), team)

    with pytest.raises(InvalidSwapError):
        game.execute_action(ActionSwapPets(0, 1), team)

    with pytest.raises(InvalidSwapError):
        game.execute_action(ActionSwapPets(1, 0), team)

    duck1 = Duck()
    team.add_pet(0, duck1)

    game.execute_action(ActionSwapPets(0, 1), team)

    assert team.pets[0] is None
    assert team.pets[1] == duck1

    duck2 = Duck()
    team.add_pet(0, duck2)

    game.execute_action(ActionSwapPets(0, 1), team)
    assert team.pets[0] == duck1
    assert team.pets[1] == duck2
