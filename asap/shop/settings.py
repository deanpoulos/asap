from typing import Optional, List, Type
from dataclasses import dataclass, field

from asap.foods import Food, TIER_1_FOODS
from asap.pets import *

DEFAULT_BUY_PRICE = 3
DEFAULT_BASE_SELL_PRICE = 1

DEFAULT_TIER_1_PET_SHOP_SIZE = 3
DEFAULT_TIER_2_PET_SHOP_SIZE = 3
DEFAULT_TIER_3_PET_SHOP_SIZE = 4
DEFAULT_TIER_4_PET_SHOP_SIZE = 4
DEFAULT_TIER_5_PET_SHOP_SIZE = 5
DEFAULT_TIER_6_PET_SHOP_SIZE = 5

DEFAULT_TIER_1_FOOD_SHOP_SIZE = 1
DEFAULT_TIER_2_FOOD_SHOP_SIZE = 1
DEFAULT_TIER_3_FOOD_SHOP_SIZE = 1
DEFAULT_TIER_4_FOOD_SHOP_SIZE = 2
DEFAULT_TIER_5_FOOD_SHOP_SIZE = 2
DEFAULT_TIER_6_FOOD_SHOP_SIZE = 2

DEFAULT_NUM_HIGHER_TIER_UNLOCKS = 2

@dataclass
class SettingsPetShop:
    PRICE_BUY_PET: Optional[int] = DEFAULT_BUY_PRICE
    PRICE_SELL_PET_BASE: Optional[int] = DEFAULT_BASE_SELL_PRICE

    NUM_HIGHER_TIER_UNLOCKS: Optional[int] = DEFAULT_NUM_HIGHER_TIER_UNLOCKS
    TIER_1_PET_SHOP_SIZE: Optional[int] = DEFAULT_TIER_1_PET_SHOP_SIZE
    TIER_2_PET_SHOP_SIZE: Optional[int] = DEFAULT_TIER_2_PET_SHOP_SIZE
    TIER_3_PET_SHOP_SIZE: Optional[int] = DEFAULT_TIER_3_PET_SHOP_SIZE
    TIER_4_PET_SHOP_SIZE: Optional[int] = DEFAULT_TIER_4_PET_SHOP_SIZE
    TIER_5_PET_SHOP_SIZE: Optional[int] = DEFAULT_TIER_5_PET_SHOP_SIZE
    TIER_6_PET_SHOP_SIZE: Optional[int] = DEFAULT_TIER_6_PET_SHOP_SIZE

    TIER_1_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_1_PETS)
    TIER_2_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_2_PETS)
    TIER_3_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_3_PETS)
    TIER_4_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_4_PETS)
    TIER_5_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_5_PETS)
    TIER_6_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_6_PETS)


@dataclass
class SettingsFoodShop:
    PRICE_BUY_FOOD: Optional[int] = DEFAULT_BUY_PRICE

    TIER_1_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_1_FOOD_SHOP_SIZE
    TIER_2_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_2_FOOD_SHOP_SIZE
    TIER_3_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_3_FOOD_SHOP_SIZE
    TIER_4_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_4_FOOD_SHOP_SIZE
    TIER_5_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_5_FOOD_SHOP_SIZE
    TIER_6_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_6_FOOD_SHOP_SIZE

    TIER_1_FOODS: Optional[List[Type[Food]]] = field(default_factory=lambda: TIER_1_FOODS)

