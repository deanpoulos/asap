import abc
from typing import Dict, Generic
from random import choice

from asap.pets import Pet
from asap.foods import Food
from .food_shop_pool import food_shop_pool
from .food_shop_size import food_shop_size
from .item import PetItem, ItemType, Item, FoodItem
from .constants import *
from .pet_shop_pool import pet_shop_pool
from .pet_shop_size import pet_shop_size
from ..engine.constants import STARTING_TURN

ItemsDict = Dict[int, None | Item[ItemType]]


class Shop(Generic[ItemType]):
    def __init__(self):
        self.items: ItemsDict = {}
        self.roll_price = DEFAULT_ROLL_PRICE

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


PetItemsDict = Dict[int, None | PetItem]
FoodItemsDict = Dict[int, None | FoodItem]


class PetShop(Shop[Pet]):
    def __init__(self):
        super().__init__()
        self.items: PetItemsDict = \
            {i: None for i in range(pet_shop_size(STARTING_TURN))}

    def refresh(self, turn: int):
        item_pool = pet_shop_pool(turn)

        for i in range(pet_shop_size(turn)):
            item = self.items[i]
            if item is None or not item.is_frozen():
                self.items[i] = PetItem(item=choice(item_pool)())


class FoodShop(Shop[Food]):
    def __init__(self):
        super().__init__()
        self.items: ItemsDict = \
            {i: None for i in range(food_shop_size(STARTING_TURN))}

    def refresh(self, turn: int):
        item_pool = food_shop_pool(turn)

        for i in range(food_shop_size(turn)):
            item = self.items[i]
            if item is None or not item.is_frozen():
                self.items[i] = FoodItem(item=choice(item_pool)())

