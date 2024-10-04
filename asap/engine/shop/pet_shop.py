from functools import lru_cache
from random import choice
from typing import List, Type

from asap.engine.pets import Pet
from asap.engine.shop.item import PetItem, HigherTierPetItem
from asap.engine.shop.settings import SettingsPetShop
from asap.engine.shop.generic_items_dict import PetItemsDict
from asap.engine.shop.generic_shop import GenericShop


class PetShop(GenericShop[Pet]):
    def __init__(self, settings: SettingsPetShop, turn: int):
        super().__init__()
        self._settings: SettingsPetShop = settings

        self.turn_pet_shop_size_unlock_mapping = {
            1: self.settings.TIER_1_PET_SHOP_SIZE,
            3: self.settings.TIER_2_PET_SHOP_SIZE,
            5: self.settings.TIER_3_PET_SHOP_SIZE,
            7: self.settings.TIER_4_PET_SHOP_SIZE,
            9: self.settings.TIER_5_PET_SHOP_SIZE,
            11: self.settings.TIER_6_PET_SHOP_SIZE
        }
        self.turn_pets_unlock_mapping = {
            1: self.settings.TIER_1_PETS,
            3: self.settings.TIER_2_PETS,
            5: self.settings.TIER_3_PETS,
            7: self.settings.TIER_4_PETS,
            9: self.settings.TIER_5_PETS,
            11: self.settings.TIER_6_PETS
        }

        self._items: PetItemsDict = \
            {i: None for i in range(self.shop_size(turn))}

    @property
    def settings(self):
        return self._settings

    def roll_new_item(self, item_pool: List[Type[Pet]]) -> PetItem:
        return PetItem(item=choice(item_pool)(), price=self.settings.PRICE_BUY_PET)

    @lru_cache(maxsize=None)
    def shop_size(self, turn: int) -> int:
        for turn_to_unlock in reversed(self.turn_pet_shop_size_unlock_mapping.keys()):
            if turn >= turn_to_unlock:
                return self.turn_pet_shop_size_unlock_mapping[turn_to_unlock]

    @lru_cache(maxsize=None)
    def shop_pool(self, turn: int, exclusive: bool = False) -> List[Type[Pet]]:
        pet_pool = []
        for turn_to_unlock in self.turn_pets_unlock_mapping.keys():
            if turn >= turn_to_unlock:
                if exclusive: pet_pool = []
                pet_pool.extend(self.turn_pets_unlock_mapping[turn_to_unlock])

        return pet_pool

    def add_higher_tier_options(self, turn: int):
        higher_tier_turn_equivalent = turn + 2
        item_pool = self.shop_pool(turn=higher_tier_turn_equivalent, exclusive=True)
        higher_tier_pet_items = [
            HigherTierPetItem(self.roll_new_item(item_pool)) for _ in range(self.settings.NUM_HIGHER_TIER_UNLOCKS)
        ]
        for item in higher_tier_pet_items:
            item.add_related_items([related_item for related_item in higher_tier_pet_items if related_item != item])

        higher_tier_options = {
            i: higher_tier_pet_items[i]
            for i in range(self.settings.NUM_HIGHER_TIER_UNLOCKS)
        }
        current_shop_pushed_back = {
            k + self.settings.NUM_HIGHER_TIER_UNLOCKS: v
            for k, v in self._items.items()
        }
        self._items = {**higher_tier_options, **current_shop_pushed_back}
