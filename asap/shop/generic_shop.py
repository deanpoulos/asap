import abc
import copy
from typing import Generic

from asap.shop.item import ItemType
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

    @abc.abstractmethod
    def refresh(self, turn: int):
        raise NotImplementedError()

    def __str__(self):
        return ', '.join([f"{item}" for index, item in self._items.items()])
