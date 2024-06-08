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
        self.items: PetItemsDict = \
            {i: None for i in range(self.pet_shop_size(turn))}

    def refresh(self, turn: int):
        item_pool = self.pet_shop_pool(turn)

        for i in range(self.pet_shop_size(turn)):
            item = self.items[i]
            if item is None or not item.is_frozen():
                self.items[i] = PetItem(item=choice(item_pool)(), price=self.settings.PRICE_BUY_PET)

    def pet_shop_size(self, turn: int) -> int:
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
    def pet_shop_pool(self, turn: int) -> List[Type[Pet]]:
        pet_pool = []
        if turn < 3:
            pet_pool.extend(self.settings.TIER_1_PETS)
        else:
            pass

        return pet_pool
