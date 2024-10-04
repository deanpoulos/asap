from types import NoneType

import numpy as np
from gymnasium.spaces import Dict, Tuple, Box, Discrete, Space, flatten_space

from asap.engine.engine.game_settings import GameSettings
from asap.engine.foods.tier1.honey import HoneyPerk
from asap.engine.foods.tokens.bread_crumbs import BreadCrumbs
from asap.engine.pets.pet import MAX_ATTACK, MAX_HEALTH, LEVEL_3_EXP
from asap.training.environment.action_masker import MAX_ACTIONS_PER_TURN


def make_observation_space(game_settings: GameSettings) -> Dict:
    pet_observation_space = make_pet_observation_space(
        max_attack=MAX_ATTACK,
        max_health=MAX_HEALTH,
        max_exp=LEVEL_3_EXP,
        max_level=game_settings.max_pet_level,
        num_pet_types=len(_all_pets(game_settings)),
        num_perk_types=len(_all_perks(game_settings))
    )

    food_observation_space = make_food_observation_space(len(_all_foods(game_settings)))

    team_observation_space = make_team_observation_space(
        pet_observation_space=pet_observation_space,
        max_starting_team_health=game_settings.starting_team_health,
        max_num_pets_per_team = game_settings.max_team_size,
    )


    pet_item_observation_space = make_pet_item_observation_space(pet_observation_space, game_settings.settings_pet_shop.MAX_ITEMS)
    food_item_observation_space = make_food_item_observation_space(food_observation_space, game_settings.settings_food_shop.MAX_ITEMS)

    pet_shop_observation_space = make_shop_observation_space(
        pet_item_observation_space,
        game_settings.settings_pet_shop.MAX_ITEMS
    )

    food_shop_observation_space = make_shop_observation_space(
        food_item_observation_space,
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
            low=np.array([0], dtype=np.int64),
            high=np.array([max_money], dtype=np.int64),
            dtype=np.int64
        ),
        "turn": Box(
            low=np.array([0], dtype=np.int64),
            high=np.array([max_turn], dtype=np.int64),
            dtype=np.int64
        ),
        "action_index": Box(
            low=np.array([0], dtype=np.int64),
            high=np.array([MAX_ACTIONS_PER_TURN], dtype=np.int64),
            dtype=np.int64
        )
    })


def make_flat_observation_space(game_settings: GameSettings):
    return flatten_space(make_observation_space(game_settings))


def make_pet_observation_space(max_health: int, max_attack: int, max_exp: int, max_level: int, num_pet_types: int, num_perk_types) -> Tuple:
    # pet_type = Discrete(num_pet_types)
    # perk_type = Discrete(num_perk_types)
    pet_type = Box(low=np.array([0]), high=np.array([num_pet_types]), dtype=np.int64)
    perk_type = Box(low=np.array([0]), high=np.array([num_perk_types]), dtype=np.int64)

    return Tuple((
        Box(
            low=np.array([0, 0, 0, 0], dtype=np.int64),
            high=np.array([max_attack, max_health, max_exp, max_level], dtype=np.int64),
            dtype=np.int64,
        ),
        pet_type,
        perk_type
    ))


def make_team_observation_space(
    pet_observation_space: Space,
    max_starting_team_health: int,
    max_num_pets_per_team: int,
) -> Dict:
    return Dict({
        "pets": Tuple([pet_observation_space for _ in range(max_num_pets_per_team)]),
        "health": Box(
            low=np.array([0], dtype=np.int64),
            high=np.array([max_starting_team_health], dtype=np.int64),
            dtype=np.int64
        ),
    })


def make_pet_item_observation_space(pet_observation_space: Space, max_price: int) -> Dict:
    return Dict({"pet": pet_observation_space, "price": Box(low=0, high=max_price, dtype=np.int64)})


def make_food_observation_space(num_foods: int) -> Box:
    # return = Discrete(num_foods)
    return Box(low=np.array([0]), high=np.array([num_foods]), dtype=np.int64)


def make_food_item_observation_space(food_observation_space: Space, max_price: int) -> Dict:
    return Dict({"food": food_observation_space, "price": Box(low=0, high=max_price, dtype=np.int64)})


def make_shop_observation_space(item_observation_space: Space, num_items_per_shop: int) -> Tuple:
    return Tuple([item_observation_space for _ in range(num_items_per_shop)])


def make_pet_observation_map(game_settings: GameSettings) -> dict:
    return {
        ability: i for i, ability in enumerate(_all_pets(game_settings))
    }

def make_perk_observation_map(game_settings: GameSettings) -> dict:
    return {
        ability: i for i, ability in enumerate(
            _all_perks(game_settings)
        )
    }

def make_food_observation_map(game_settings: GameSettings) -> dict:
    return {
        ability: i for i, ability in enumerate(
            _all_foods(game_settings)
        )
    }

def _all_pets(game_settings: GameSettings):
    return [NoneType] + game_settings.settings_pet_shop.all_pets()

def _all_foods(game_settings: GameSettings):
    return game_settings.settings_food_shop.all_foods() + [BreadCrumbs]

def _all_perks(game_settings: GameSettings):
    return [NoneType, HoneyPerk]