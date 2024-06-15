from functools import lru_cache
from random import choice
from typing import List, Type

from asap.foods import Food
from .item import FoodItem
from .settings import SettingsFoodShop
from .generic_items_dict import ItemsDict
from .generic_shop import GenericShop


class FoodShop(GenericShop[Food]):
    def __init__(self, settings: SettingsFoodShop, turn: int):
        super().__init__()
        self.settings: SettingsFoodShop = settings
        self._items: ItemsDict = \
            {i: None for i in range(self.shop_size(turn))}

    def roll_new_item(self, item_pool: List[Type[Food]]) -> FoodItem:
        return FoodItem(item=choice(item_pool)(), price=self.settings.PRICE_BUY_FOOD)

    def shop_size(self, turn: int) -> int:
        if turn < 3:
            return self.settings.TIER_1_FOOD_SHOP_SIZE
        elif turn < 5:
            return self.settings.TIER_2_FOOD_SHOP_SIZE
        elif turn < 7:
            return self.settings.TIER_3_FOOD_SHOP_SIZE
        elif turn < 9:
            return self.settings.TIER_4_FOOD_SHOP_SIZE
        elif turn < 11:
            return self.settings.TIER_5_FOOD_SHOP_SIZE
        else:
            return self.settings.TIER_6_FOOD_SHOP_SIZE

    @lru_cache(maxsize=None)
    def shop_pool(self, turn: int) -> List[Type[Food]]:
        item_pool = []
        if turn >= 1:
            item_pool.extend(self.settings.TIER_1_FOODS)

        return item_pool
