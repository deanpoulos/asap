from typing import Type, List

from asap.pets import TIER_1_PETS, Pet

from functools import lru_cache


@lru_cache(maxsize=None)
def pet_shop_pool(turn: int) -> List[Type[Pet]]:
    pet_pool = []
    if turn < 3:
        pet_pool.extend(TIER_1_PETS)
    # elif turn < 5:
    #     pet_pool.extend(TIER_2_PETS)
    # elif turn < 7:
    #     pet_pool.extend(TIER_3_PETS)
    # elif turn < 9:
    #     pet_pool.extend(TIER_4_PETS)
    # elif turn < 11:
    #     pet_pool.extend(TIER_5_PETS)
    # else:
    #     pet_pool.extend(TIER_6_PETS)

    return pet_pool

