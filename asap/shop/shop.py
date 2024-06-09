from .food_shop import FoodShop
from .pet_shop import PetShop
from .settings import SettingsPetShop, SettingsFoodShop


class Shop:
    def __init__(self,
                 settings_pet_shop: SettingsPetShop,
                 settings_food_shop: SettingsFoodShop,
                 roll_price: int,
                 turn: int):
        self.roll_price: int = roll_price
        self.pet_shop: PetShop = PetShop(settings_pet_shop, turn)
        self.food_shop: FoodShop = FoodShop(settings_food_shop, turn)

    def __str__(self):
        return f"{self.pet_shop} | {self.food_shop}"

    def refresh(self, turn: int):
        self.pet_shop.refresh(turn)
        self.food_shop.refresh(turn)
