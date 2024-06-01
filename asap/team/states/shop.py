from dataclasses import dataclass, field

from asap.shop import PetShop, FoodShop
from asap.team.team import Team


STARTING_MONEY = 10


@dataclass
class TeamShopState:
    team: Team
    pet_shop: PetShop = field(default_factory=PetShop)
    food_shop: FoodShop = field(default_factory=FoodShop)
    money: int = STARTING_MONEY
