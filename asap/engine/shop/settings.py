from typing import Optional, List, Type
from dataclasses import dataclass, field

from asap.engine.foods import Food, TIER_1_FOODS
from asap.engine.pets import *

DEFAULT_BUY_PRICE = 3
DEFAULT_BASE_SELL_PRICE = 1

DEFAULT_MAX_PET_ITEMS = 9

DEFAULT_TIER_1_PET_SHOP_SIZE = 3
DEFAULT_TIER_2_PET_SHOP_SIZE = 3
DEFAULT_TIER_3_PET_SHOP_SIZE = 4
DEFAULT_TIER_4_PET_SHOP_SIZE = 4
DEFAULT_TIER_5_PET_SHOP_SIZE = 5
DEFAULT_TIER_6_PET_SHOP_SIZE = 5

DEFAULT_MAX_FOOD_ITEMS = 7

DEFAULT_TIER_1_FOOD_SHOP_SIZE = 1
DEFAULT_TIER_2_FOOD_SHOP_SIZE = 1
DEFAULT_TIER_3_FOOD_SHOP_SIZE = 2
DEFAULT_TIER_4_FOOD_SHOP_SIZE = 2
DEFAULT_TIER_5_FOOD_SHOP_SIZE = 2
DEFAULT_TIER_6_FOOD_SHOP_SIZE = 2

DEFAULT_NUM_HIGHER_TIER_UNLOCKS = 2

@dataclass
class SettingsPetShop:
    PRICE_BUY_PET: Optional[int] = DEFAULT_BUY_PRICE
    PRICE_SELL_PET_BASE: Optional[int] = DEFAULT_BASE_SELL_PRICE
    MAX_ITEMS: Optional[int] = DEFAULT_MAX_PET_ITEMS

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

    def all_pets(self) -> List[Type[Pet]]:
        return self.TIER_1_PETS + self.TIER_2_PETS + self.TIER_3_PETS + self.TIER_4_PETS + self.TIER_5_PETS +  self.TIER_6_PETS

    def num_possible_pets(self) -> int:
        return len(self.all_pets())


@dataclass
class SettingsFoodShop:
    PRICE_BUY_FOOD: Optional[int] = DEFAULT_BUY_PRICE
    MAX_ITEMS: Optional[int] = DEFAULT_MAX_FOOD_ITEMS

    TIER_1_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_1_FOOD_SHOP_SIZE
    TIER_2_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_2_FOOD_SHOP_SIZE
    TIER_3_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_3_FOOD_SHOP_SIZE
    TIER_4_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_4_FOOD_SHOP_SIZE
    TIER_5_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_5_FOOD_SHOP_SIZE
    TIER_6_FOOD_SHOP_SIZE: Optional[int] = DEFAULT_TIER_6_FOOD_SHOP_SIZE

    TIER_1_FOODS: Optional[List[Type[Food]]] = field(default_factory=lambda: TIER_1_FOODS)

    def all_foods(self) -> List[Type[Food]]:
        return self.TIER_1_FOODS

    def num_possible_foods(self) -> int:
        return len(self.all_foods())
