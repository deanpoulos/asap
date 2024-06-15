import abc
import copy
from typing import Generic, List, Type

from asap.shop.item import ItemType, Item
from asap.shop.generic_items_dict import ItemsDict


class GenericShop(Generic[ItemType]):
    def __init__(self):
        self._items: ItemsDict = {}

    @property
    def items(self):
        return {i: item for i, item in self._items.items() if item is not None}

    def freeze(self, index: int):
        self._items[index].freeze()

    def unfreeze(self, index: int):
        self._items[index].unfreeze()

    def buy(self, index: int) -> ItemType:
        bought_item = self._items[index].item
        self._items[index] = None

        return bought_item

    def price(self, index: int) -> int:
        return self._items[index].price

    def already_bought(self, index: int) -> bool:
        return self._items[index] is None

    def refresh(self, turn: int):
        item_pool = self.shop_pool(turn)

        frozen_items = [item for item in self.items.values() if item.is_frozen()]

        refreshed_items = []
        for _ in range(self.shop_size(turn) - len(frozen_items)):
            refreshed_items.append(self.roll_new_item(item_pool))

        new_shop_items = frozen_items + refreshed_items

        self._items = {}
        for i in range(max(self.shop_size(turn), len(new_shop_items))):
            self._items[i] = new_shop_items[i]

    @abc.abstractmethod
    def shop_size(self, turn: int) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def shop_pool(self, turn: int, exclusive: bool = False) -> List[Type[ItemType]]:
        raise NotImplementedError()

    def roll_new_item(self, item_pool: List[Type[ItemType]]) -> Item[ItemType]:
        raise NotImplementedError()

    def __str__(self):
        return ', '.join([f"{item}" for index, item in self._items.items()])
