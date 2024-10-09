import typing

import gymnasium.spaces
from gymnasium import spaces

from types import NoneType

import numpy as np
from gymnasium.spaces import Dict, Tuple, Box, Discrete, Space, flatten_space

from asap.engine.engine.game_settings import GameSettings
from asap.engine.foods.tier1.honey import HoneyPerk
from asap.engine.foods.tokens.bread_crumbs import BreadCrumbs
from asap.engine.pets.pet import MAX_ATTACK, MAX_HEALTH, LEVEL_3_EXP
from asap.training.environment.action_masker import MAX_ACTIONS_PER_TURN


def make_observation_space(game_settings: GameSettings, observe_opponent_after_battle: bool = True) -> Dict:
    observation_space = make_full_observation_space(game_settings, observe_opponent_after_battle)

    new_observation_space = gymnasium.spaces.Dict()

    team_observation_space = observation_space.spaces.pop("team_left")
    new_observation_space.spaces.update(
        **{f"team_left_{key}": value for key, value in team_observation_space.spaces.items()},
    )

    if observe_opponent_after_battle:
        opponent_observation_space = observation_space.spaces.pop("team_right")
        new_observation_space.spaces.update(
            **{f"team_right_{key}": value for key, value in opponent_observation_space.spaces.items()}
        )

    pet_shop_observation_space = observation_space.spaces.pop("pet_shop")
    new_observation_space.spaces.update(
        **{f"pet_shop_{i}": value for i, value in enumerate(pet_shop_observation_space.spaces)},
    )

    food_shop_observation_space = observation_space.spaces.pop("food_shop")
    new_observation_space.spaces.update(
        **{f"food_shop_{i}": value for i, value in enumerate(food_shop_observation_space.spaces)},
    )

    new_observation_space.spaces.update(
        **observation_space
    )

    return new_observation_space


def make_full_observation_space(game_settings: GameSettings, observe_opponent_after_battle: bool = True) -> Dict:
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

    opponent_observation = {}
    if observe_opponent_after_battle:
        opponent_observation = {"team_right": team_observation_space}

    observation_space = Dict({
        "team_left": team_observation_space,
        **opponent_observation,
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

    return observation_space

def make_flat_observation_space(game_settings: GameSettings, observe_opponent_after_battle: bool = True) -> Dict:
    observation_space = make_observation_space(game_settings, observe_opponent_after_battle)
    for key, subspace in observation_space.spaces.items():
        if isinstance(subspace, (Tuple, Dict)):
            observation_space.spaces[key] = flatten_space(subspace)

    return observation_space


def make_pet_observation_space(max_health: int, max_attack: int, max_exp: int, max_level: int, num_pet_types: int, num_perk_types) -> Tuple:
    pet_type = Discrete(num_pet_types)
    perk_type = Discrete(num_perk_types)
    # pet_type = Box(low=np.array([0]), high=np.array([num_pet_types]), dtype=np.int64)
    # perk_type = Box(low=np.array([0]), high=np.array([num_perk_types]), dtype=np.int64)

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
        **{f"pet_{i}": pet_observation_space for i in range(max_num_pets_per_team)},
        "health": Box(
            low=np.array([0], dtype=np.int64),
            high=np.array([max_starting_team_health], dtype=np.int64),
            dtype=np.int64
        ),
    })


def make_pet_item_observation_space(pet_observation_space: Space, max_price: int) -> Tuple:
    price_observation_space = Box(low=0, high=max_price, dtype=np.int64)
    return Tuple([pet_observation_space, price_observation_space])


def make_food_observation_space(num_foods: int) -> Discrete:
    return Discrete(num_foods)


def make_food_item_observation_space(food_observation_space: Space, max_price: int) -> Tuple:
    price_observation_space = Box(low=0, high=max_price, dtype=np.int64)
    return Tuple([food_observation_space, price_observation_space])


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

def _all_perks(_: GameSettings):
    return [NoneType, HoneyPerk]


def get_observation_dim_names(space: typing.Union[spaces.Dict, spaces.Tuple], base_name: str = 'obs',
                              dim_names: typing.List[str] = None):
    if dim_names is None:
        dim_names = []

    if isinstance(space, spaces.Box):
        for i in range(space.shape[0]):
            dim_names.append(f"{base_name}/{i}")
    elif isinstance(space, spaces.Discrete):
        for i in range(space.n):
            dim_names.append(f"{base_name}={i}")
    elif isinstance(space, spaces.Tuple):
        for i, space in enumerate(space.spaces):
            get_observation_dim_names(space, f"{base_name}/{i}", dim_names)
    elif isinstance(space, spaces.Dict):
        for name, space in space.items():
            get_observation_dim_names(space, f"{base_name}/{name}", dim_names)

    else:
        raise NotImplementedError(f"Expected Box, Discrete, Tuple, Dict, got space type {type(space)}")

    return dim_names