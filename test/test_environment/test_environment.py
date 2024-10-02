import numpy as np

from asap.engine.actions import ActionRefreshShop
from asap.environment.action_masker import mask_fn
from asap.environment.action_space import make_action_space, make_possible_actions
from asap.environment.environment import AsapEnvironmentTwoPlayer


def test_environment_init(game_turn_1_2_teams):
    env = AsapEnvironmentTwoPlayer(game_turn_1_2_teams.settings)

    assert env.action_index == 0
    for i in range(game_turn_1_2_teams.settings.settings_pet_shop.num_possible_pets()):
        assert env.pet_observation_map[game_turn_1_2_teams.settings.settings_pet_shop.all_pets()[i]] == i
    for i in range(game_turn_1_2_teams.settings.settings_food_shop.num_possible_foods()):
        assert env.food_observation_map[game_turn_1_2_teams.settings.settings_food_shop.all_foods()[i]] == i

    assert env.team_left == env.game.teams[0]
    assert env.team_right == env.game.teams[1]

def test_environment_basic_observation(game_turn_1_2_teams):
    env = AsapEnvironmentTwoPlayer(game_turn_1_2_teams.settings)

    obs, reward, terminated, truncated, info = env.step(env.action_map_inverse[ActionRefreshShop()])

    assert obs["turn"] == game_turn_1_2_teams.settings.starting_turn
    assert obs["money"] == game_turn_1_2_teams.settings.starting_money - 1
    assert obs["team_left"]["health"] == game_turn_1_2_teams.settings.starting_team_health
    assert obs["team_right_last_state"]["health"] == game_turn_1_2_teams.settings.starting_team_health
    for i in range(game_turn_1_2_teams.settings.max_pet_level):
        assert obs["team_left"]["pets"][i] == [0, 0, 0, 0, 0]
        assert obs["team_right_last_state"]["pets"][i] == [0, 0, 0, 0, 0]
    assert terminated == False
    assert truncated == False

def test_action_space(game_turn_1_2_teams):
    possible_actions = make_possible_actions(game_turn_1_2_teams.settings)

    team_size = game_turn_1_2_teams.settings.max_team_size
    pet_shop_size = game_turn_1_2_teams.settings.settings_pet_shop.MAX_ITEMS
    food_shop_size = game_turn_1_2_teams.settings.settings_food_shop.MAX_ITEMS

    assert len(possible_actions) == (
        2 +  # refresh/end
        2*pet_shop_size + 2*food_shop_size + # freezing
        team_size + 2*(team_size**2 - team_size) +  # sell, merge/swap
        2*pet_shop_size*team_size + food_shop_size*team_size  # buy and place/merge/apply food
    )

def test_action_mask(game_turn_1_2_teams):
    env = AsapEnvironmentTwoPlayer(game_turn_1_2_teams.settings)

    action_mask = mask_fn(env)

    team_size = game_turn_1_2_teams.settings.max_team_size
    pet_shop_size = game_turn_1_2_teams.settings.settings_pet_shop.MAX_ITEMS
    food_shop_size = game_turn_1_2_teams.settings.settings_food_shop.MAX_ITEMS

    num_starting_pets = game_turn_1_2_teams.settings.settings_pet_shop.TIER_1_PET_SHOP_SIZE
    num_starting_foods = game_turn_1_2_teams.settings.settings_food_shop.TIER_1_FOOD_SHOP_SIZE

    exp = np.array([
        1,  # can refresh
        1,  # can end turn
        *[1, 0]*(num_starting_pets),  # can freeze, can't unfreeze all pets in shop
        *[0, 0]*(pet_shop_size - num_starting_pets),  # can freeze non-existent pets
        *[1, 0]*(num_starting_foods),
        *[0, 0]*(food_shop_size - num_starting_foods),
        *[0]*team_size,  # can't sell any pets yet
        *[0]*2*(team_size**2 - team_size),  # can't merge or swap pets yet
        *[1, 0]*num_starting_pets*team_size,  # can buy and place any pets in any position
        *[0, 0]*(pet_shop_size - num_starting_pets)*team_size,
        *[0]*(food_shop_size * team_size)  # can't apply foods to no pets
    ], dtype=int)

    assert np.all(action_mask == exp)