from functools import lru_cache
from random import choice
from typing import List, Type

from asap.pets import Pet
from asap.shop.item import PetItem
from asap.shop.settings import SettingsPetShop
from asap.shop.generic_items_dict import PetItemsDict
from asap.shop.generic_shop import GenericShop


class PetShop(GenericShop[Pet]):
    def __init__(self, settings: SettingsPetShop, turn: int):
        super().__init__()
        self.settings: SettingsPetShop = settings
        self._items: PetItemsDict = \
            {i: None for i in range(self.shop_size(turn))}

    def roll_new_item(self, item_pool: List[Type[Pet]]) -> PetItem:
        return PetItem(item=choice(item_pool)(), price=self.settings.PRICE_BUY_PET)

    def shop_size(self, turn: int) -> int:
        if turn < 3:
            return self.settings.TIER_1_PET_SHOP_SIZE
        elif turn < 5:
            return self.settings.TIER_2_PET_SHOP_SIZE
        elif turn < 7:
            return self.settings.TIER_3_PET_SHOP_SIZE
        elif turn < 9:
            return self.settings.TIER_4_PET_SHOP_SIZE
        elif turn < 11:
            return self.settings.TIER_5_PET_SHOP_SIZE
        else:
            return self.settings.TIER_6_PET_SHOP_SIZE

    @lru_cache(maxsize=None)
    def shop_pool(self, turn: int) -> List[Type[Pet]]:
        pet_pool = []
        if turn > 1:
            pet_pool.extend(self.settings.TIER_1_PETS)
        if turn > 3:
            pet_pool.extend(self.settings.TIER_2_PETS)
        if turn > 5:
            pet_pool.extend(self.settings.TIER_3_PETS)
        if turn > 7:
            pet_pool.extend(self.settings.TIER_4_PETS)
        if turn > 9:
            pet_pool.extend(self.settings.TIER_5_PETS)
        if turn > 11:
            pet_pool.extend(self.settings.TIER_6_PETS)

        return pet_pool

    def add_higher_tier_options(self, turn: int):
        higher_tier_turn_equivalent = turn + 2
        item_pool = self.shop_pool(turn=higher_tier_turn_equivalent)
        higher_tier_options = {
            i: self.roll_new_item(item_pool)
            for i in range(self.settings.NUM_HIGHER_TIER_UNLOCKS)
        }
        current_shop_pushed_back = {
            k + self.settings.NUM_HIGHER_TIER_UNLOCKS: v
            for k, v in self._items.items()
        }
        self._items = {**higher_tier_options, **current_shop_pushed_back}
