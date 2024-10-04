import numpy as np

from asap.engine.actions import ActionRefreshShop, ActionBuyAndPlacePet, ActionFreezePet, ActionSellPet, ActionSwapPets, \
    ActionBuyFood
from asap.training.environment.action_masker import mask_fn
from asap.training.environment.action_space import make_possible_actions
from asap.training.environment.environment import AsapEnvironmentTwoPlayer


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

    assert np.all(exp == action_mask)

    env.step(env.action_map_inverse[ActionBuyAndPlacePet(0, 0)])

    action_mask = mask_fn(env)
    invalid_actions = [
        # can't freeze pet after bought
        ActionFreezePet(0),
        # can't unfreeze pet after bought
        ActionFreezePet(0),
        # can't put a pet in position 0
        ActionBuyAndPlacePet(1, 0),
        ActionBuyAndPlacePet(2, 0),
        # can't rebuy bought pet
        ActionBuyAndPlacePet(0, 1),
    ]

    for invalid_action in invalid_actions:
        assert action_mask[env.action_map_inverse[invalid_action]] == 0

    valid_actions = [
        # can sell pet after bought
        ActionSellPet(0),
        # can swap pet after bought
        ActionSwapPets(0, 1),
        ActionSwapPets(0, 2),
        ActionSwapPets(0, 3),
        ActionSwapPets(0, 4),
        ActionSwapPets(4, 0),
        ActionSwapPets(3, 0),
        ActionSwapPets(2, 0),
        ActionSwapPets(1, 0),
        # can give pet food
        ActionBuyFood(0, 0),
    ]

    for valid_action in valid_actions:
        assert action_mask[env.action_map_inverse[valid_action]] == 1
