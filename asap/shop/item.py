from typing import TypeVar, Generic

from asap.foods.food import Food
from asap.pets import Pet

ItemType = TypeVar('ItemType')


class Item(Generic[ItemType]):
    def __init__(self, item: ItemType, price: int):
        self.item: ItemType = item
        self.price: int = price
        self._frozen: bool = False

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    def is_frozen(self) -> bool:
        return self._frozen

    def __str__(self):
        return f"${self.price} {self.item}" \
               f'{" (frozen)" if self.is_frozen() else ""}'


class PetItem(Item[Pet]):
    def __init__(self, item: Pet, price: int):
        super().__init__(item, price)


class FoodItem(Item[Food]):
    def __init__(self, item: Food, price: int):
        super().__init__(item, price)

