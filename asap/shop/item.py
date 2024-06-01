from typing import Type

from asap.engine.pets import Pet


DEFAULT_PRICE = 3


class Item:
    def __init__(self, price: int = DEFAULT_PRICE):
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


class PetItem(Item):
    def __init__(self, pet: Type[Pet]):
        super().__init__()
        self.pet: Type[Pet] = pet

    def __str__(self):
        return f"${self.price}: {self.pet}" \
               f'{" (frozen)" if self.is_frozen() else ""}' \
               f'{" SOLD!" if self.already_bought() else ""}'
