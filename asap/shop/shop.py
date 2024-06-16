from .food_shop import FoodShop
from .pet_shop import PetShop
from .settings import SettingsPetShop, SettingsFoodShop
from ..engine.shop.subscribers.pet_subscriber import PetSubscriber


class Shop(PetSubscriber):
    def __init__(self,
                 settings_pet_shop: SettingsPetShop,
                 settings_food_shop: SettingsFoodShop,
                 roll_price: int,
                 turn: int):
        super().__init__()
        self.roll_price: int = roll_price
        self.pet_shop: PetShop = PetShop(settings_pet_shop, turn)
        self.food_shop: FoodShop = FoodShop(settings_food_shop, turn)
        self.turn = turn

    def __str__(self):
        return f"{self.pet_shop} | {self.food_shop}"

    def refresh(self):
        self.pet_shop.refresh(self.turn)
        self.food_shop.refresh(self.turn)

    def notify_level_change(self):
        self.add_higher_tier_pet_options()

    def add_higher_tier_pet_options(self):
        self.pet_shop.add_higher_tier_options(self.turn)

    def buy_pet(self, shop_index: int):
        pet = self.pet_shop.buy(shop_index)
        pet.add_subscriber(self)

        return pet

    def buy_food(self, shop_index: int):
        return self.food_shop.buy(shop_index)
