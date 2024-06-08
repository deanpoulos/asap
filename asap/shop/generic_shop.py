import abc
from typing import Generic

from asap.shop.item import ItemType
from asap.shop.generic_items_dict import ItemsDict


class GenericShop(Generic[ItemType]):
    def __init__(self):
        self.items: ItemsDict = {}

    def freeze(self, index: int):
        self.items[index].freeze()

    def unfreeze(self, index: int):
        self.items[index].unfreeze()

    def buy(self, index: int) -> ItemType:
        bought_item = self.items[index].item
        self.items[index].buy()

        return bought_item

    def price(self, index: int) -> int:
        return self.items[index].price

    def already_bought(self, index: int) -> bool:
        return self.items[index].already_bought()

    @abc.abstractmethod
    def refresh(self, turn: int):
        raise NotImplementedError()

    def __str__(self):
        return '\n'.join([f"{index}: {item}" for index, item in self.items.items()])
