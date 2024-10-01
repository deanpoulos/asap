from asap.engine.actions import ActionRefreshShop
from asap.environment.environment import AsapEnvironmentTwoPlayer


def test_environment_init(game_turn_1_2_teams):
    env = AsapEnvironmentTwoPlayer(game_turn_1_2_teams.settings)

    assert env.action_index == 0
    for i in range(game_turn_1_2_teams.settings.settings_pet_shop.num_possible_pets()):
        assert env._pet_observation_map[game_turn_1_2_teams.settings.settings_pet_shop.all_pets()[i]] == i
    for i in range(game_turn_1_2_teams.settings.settings_food_shop.num_possible_foods()):
        assert env._food_observation_map[game_turn_1_2_teams.settings.settings_food_shop.all_foods()[i]] == i

    assert env.team_left == env.game.teams[0]
    assert env.team_right == env.game.teams[1]

def test_environment_basic_observation(game_turn_1_2_teams):
    env = AsapEnvironmentTwoPlayer(game_turn_1_2_teams.settings)

    obs, reward, terminated, truncated, info = env.step(ActionRefreshShop())

    assert obs["turn"] == game_turn_1_2_teams.settings.starting_turn
    assert obs["money"] == game_turn_1_2_teams.settings.starting_money - 1
    assert obs["team_left"]["health"] == game_turn_1_2_teams.settings.starting_team_health
    assert obs["team_right_last_state"]["health"] == game_turn_1_2_teams.settings.starting_team_health
    for i in range(game_turn_1_2_teams.settings.max_pet_level):
        assert obs["team_left"]["pets"][i] == [0, 0, 0, 0, 0]
        assert obs["team_right_last_state"]["pets"][i] == [0, 0, 0, 0, 0]
    assert terminated == False
    assert truncated == False
