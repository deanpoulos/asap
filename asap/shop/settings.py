from typing import Optional, List, Type
from dataclasses import dataclass, field

from asap.foods import Food, TIER_1_FOODS
from asap.pets import Pet, TIER_1_PETS

DEFAULT_BUY_PRICE = 3
DEFAULT_BASE_SELL_PRICE = 1

TIER_1_PET_SHOP_SIZE = 3
TIER_2_PET_SHOP_SIZE = 3
TIER_3_PET_SHOP_SIZE = 4
TIER_4_PET_SHOP_SIZE = 4
TIER_5_PET_SHOP_SIZE = 5
TIER_6_PET_SHOP_SIZE = 5

TIER_1_FOOD_SHOP_SIZE = 1
TIER_2_FOOD_SHOP_SIZE = 1
TIER_3_FOOD_SHOP_SIZE = 1
TIER_4_FOOD_SHOP_SIZE = 2
TIER_5_FOOD_SHOP_SIZE = 2
TIER_6_FOOD_SHOP_SIZE = 2


@dataclass
class SettingsPetShop:
    PRICE_BUY_PET: Optional[int] = DEFAULT_BUY_PRICE
    PRICE_SELL_PET_BASE: Optional[int] = DEFAULT_BASE_SELL_PRICE

    TIER_1_PET_SHOP_SIZE: Optional[int] = TIER_1_PET_SHOP_SIZE
    TIER_2_PET_SHOP_SIZE: Optional[int] = TIER_2_PET_SHOP_SIZE
    TIER_3_PET_SHOP_SIZE: Optional[int] = TIER_3_PET_SHOP_SIZE
    TIER_4_PET_SHOP_SIZE: Optional[int] = TIER_4_PET_SHOP_SIZE
    TIER_5_PET_SHOP_SIZE: Optional[int] = TIER_5_PET_SHOP_SIZE
    TIER_6_PET_SHOP_SIZE: Optional[int] = TIER_6_PET_SHOP_SIZE

    TIER_1_PETS: Optional[List[Type[Pet]]] = field(default_factory=lambda: TIER_1_PETS)


@dataclass
class SettingsFoodShop:
    PRICE_BUY_FOOD: Optional[int] = DEFAULT_BUY_PRICE

    TIER_1_FOOD_SHOP_SIZE: Optional[int] = TIER_1_FOOD_SHOP_SIZE
    TIER_2_FOOD_SHOP_SIZE: Optional[int] = TIER_2_FOOD_SHOP_SIZE
    TIER_3_FOOD_SHOP_SIZE: Optional[int] = TIER_3_FOOD_SHOP_SIZE
    TIER_4_FOOD_SHOP_SIZE: Optional[int] = TIER_4_FOOD_SHOP_SIZE
    TIER_5_FOOD_SHOP_SIZE: Optional[int] = TIER_5_FOOD_SHOP_SIZE
    TIER_6_FOOD_SHOP_SIZE: Optional[int] = TIER_6_FOOD_SHOP_SIZE

    TIER_1_FOODS: Optional[List[Type[Food]]] = field(default_factory=lambda: TIER_1_FOODS)

