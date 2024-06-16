import typing
from typing import TypeVar, Generic, List

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


class HigherTierPetItem(PetItem):
    def __init__(self, pet_item: PetItem):
        super().__init__(item=pet_item.item, price=pet_item.price)
        self.related_items = []

    def add_related_items(self, related_items: List[typing.Self]):
        self.related_items = related_items


class FoodItem(Item[Food]):
    def __init__(self, item: Food, price: int):
        super().__init__(item, price)

