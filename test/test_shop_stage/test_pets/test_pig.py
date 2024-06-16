from asap.actions import ActionSellPet
from asap.engine.game_settings import DEFAULT_STARTING_MONEY
from asap.pets import Pig
from asap.pets.pet import LEVEL_2_EXP, LEVEL_3_EXP


def test_pig_on_sell(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    state = game.team_states[team]

    team.add_pet(0, Pig())
    game.execute_action(ActionSellPet(0), team)

    # +1 for sale, +1 for on-sell ability
    assert state.money == DEFAULT_STARTING_MONEY + 1 + 1

    team.add_pet(0, Pig(exp=LEVEL_2_EXP))
    game.execute_action(ActionSellPet(0), team)

    # additional +2 for sale, +2 for on-sell ability
    assert state.money == DEFAULT_STARTING_MONEY + 1 + 1 + 2 + 2

    team.add_pet(0, Pig(exp=LEVEL_3_EXP))
    game.execute_action(ActionSellPet(0), team)

    # additional +3 for sale, +3 for on-sell ability
    assert state.money == DEFAULT_STARTING_MONEY + 1 + 1 + 2 + 2 + 3 + 3
