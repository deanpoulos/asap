from typing import TypeVar, Generic

from asap.foods.food import Food
from asap.pets import Pet


DEFAULT_PRICE = 3


ItemType = TypeVar('ItemType')


class Item(Generic[ItemType]):
    def __init__(self, item: ItemType, price: int = DEFAULT_PRICE):
        self.item: ItemType = item
        self.price: int = price
        self._frozen: bool = False
        self._bought: bool = False

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    def is_frozen(self) -> bool:
        return self._frozen

    def buy(self):
        self._bought = True

    def already_bought(self):
        return self._bought

    def __str__(self):
        return f"${self.price}: {self.item}" \
               f'{" (frozen)" if self.is_frozen() else ""}' \
               f'{" SOLD!" if self.already_bought() else ""}'


class PetItem(Item[Pet]):
    def __init__(self, item: Pet):
        super().__init__(item)


class FoodItem(Item[Food]):
    def __init__(self, item: Food):
        super().__init__(item)

