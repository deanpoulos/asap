from typing import Type, List

from functools import lru_cache

from asap.foods.food import Food
from asap.foods.tier1 import TIER_1_FOODS


@lru_cache(maxsize=None)
def food_shop_pool(turn: int) -> List[Type[Food]]:
    pet_pool = []
    if turn < 3:
        pet_pool.extend(TIER_1_FOODS)
    # elif turn < 5:
    #     pet_pool.extend(TIER_2_FOODS)
    # elif turn < 7:
    #     pet_pool.extend(TIER_3_FOODS)
    # elif turn < 9:
    #     pet_pool.extend(TIER_4_FOODS)
    # elif turn < 11:
    #     pet_pool.extend(TIER_5_FOODS)
    # else:
    #     pet_pool.extend(TIER_6_FOODS)

    return pet_pool

