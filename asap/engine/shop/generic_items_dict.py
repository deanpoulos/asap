from typing import Dict

from asap.engine.shop.item import Item, ItemType, PetItem, FoodItem

ItemsDict = Dict[int, None | Item[ItemType]]
PetItemsDict = Dict[int, None | PetItem]
FoodItemsDict = Dict[int, None | FoodItem]
