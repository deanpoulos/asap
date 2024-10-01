import numpy as np
from gym.spaces import Dict, Tuple, Box, Discrete, Space

from asap.engine.engine.game_settings import GameSettings
from asap.engine.pets.pet import MAX_ATTACK, MAX_HEALTH, LEVEL_3_EXP


def make_observation_space(game_settings: GameSettings) -> Dict:
    pet_observation_space = make_pet_observation_space(
        max_attack=MAX_ATTACK,
        max_health=MAX_HEALTH,
        max_exp=LEVEL_3_EXP,
        max_level=game_settings.max_pet_level,
        num_pet_abilities=game_settings.settings_pet_shop.num_possible_pets()
    )

    team_observation_space = make_team_observation_space(
        pet_observation_space=pet_observation_space,
        max_starting_team_health=game_settings.starting_team_health,
        max_num_pets_per_team = game_settings.max_team_size,
    )

    food_observation_space = make_food_observation_space(game_settings.settings_food_shop.num_possible_foods())

    pet_shop_observation_space = make_shop_observation_space(
        pet_observation_space,
        game_settings.settings_pet_shop.MAX_ITEMS
    )

    food_shop_observation_space = make_shop_observation_space(
        food_observation_space,
        game_settings.settings_food_shop.MAX_ITEMS
    )

    max_money = game_settings.max_money
    max_turn = game_settings.max_turn

    return Dict({
        "team_left": team_observation_space,
        "team_right": team_observation_space,
        "pet_shop": pet_shop_observation_space,
        "food_shop": food_shop_observation_space,
        "money": Box(
            low=np.array([0], dtype=np.int32),
            high=np.array([max_money], dtype=np.int32),
            dtype=np.int32
        ),
        "turn": Box(
            low=np.array([0], dtype=np.int32),
            high=np.array([max_turn], dtype=np.int32),
            dtype=np.int32
        ),
    })


def make_pet_observation_space(max_health: int, max_attack: int, max_exp: int, max_level: int, num_pet_abilities: int) -> Tuple:
    ability_observation_space = Discrete(num_pet_abilities)

    return Tuple((
        Box(
            low=np.array([0, 0, 0, 0], dtype=np.int32),
            high=np.array([max_attack, max_health, max_exp, max_level], dtype=np.int32),
            dtype=np.int32,
        ),
        ability_observation_space
    ))


def make_team_observation_space(
    pet_observation_space: Space,
    max_starting_team_health: int,
    max_num_pets_per_team: int,
) -> Dict:
    return Dict({
        "pets": Tuple([pet_observation_space for _ in range(max_num_pets_per_team)]),
        "health": Box(
            low=np.array([0], dtype=np.int32),
            high=np.array([max_starting_team_health], dtype=np.int32),
            dtype=np.int32
        ),
    })


def make_pet_item_observation_space(pet_observation_space: Space, max_price: int) -> Dict:
    return Dict({"pet": pet_observation_space, "price": Box(low=0, high=max_price, dtype=np.int32)})


def make_food_observation_space(num_foods: int) -> Discrete:
    return Discrete(num_foods)


def make_food_item_observation_space(food_observation_space: Space, max_price: int) -> Dict:
    return Dict({"food": food_observation_space, "price": Box(low=0, high=max_price, dtype=np.int32)})


def make_shop_observation_space(item_observation_space: Space, num_items_per_shop: int) -> Tuple:
    return Tuple([item_observation_space for _ in range(num_items_per_shop)])


def make_pet_observation_map(game_settings: GameSettings) -> dict:
    return {
        ability: i for i, ability in enumerate(game_settings.settings_pet_shop.all_pets())
    }

def make_food_observation_map(game_settings: GameSettings) -> dict:
    return {
        ability: i for i, ability in enumerate(game_settings.settings_food_shop.all_foods())
    }
