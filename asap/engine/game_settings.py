from dataclasses import dataclass, field
from typing import Optional

from asap.shop.settings import SettingsPetShop, SettingsFoodShop


DEFAULT_ROLL_PRICE = 1
DEFAULT_STARTING_TURN = 1
DEFAULT_MAX_TEAM_SIZE = 5
DEFAULT_STARTING_TEAM_HEALTH = 6
DEFAULT_MAX_PET_LEVEL = 3
DEFAULT_STARTING_MONEY = 10


@dataclass
class GameSettings:
    roll_price: Optional[int] = DEFAULT_ROLL_PRICE
    starting_turn: Optional[int] = DEFAULT_STARTING_TURN
    max_team_size: Optional[int] = DEFAULT_MAX_TEAM_SIZE
    starting_team_health: Optional[int] = DEFAULT_STARTING_TEAM_HEALTH
    max_pet_level: Optional[int] = DEFAULT_MAX_PET_LEVEL
    starting_money: Optional[int] = DEFAULT_STARTING_MONEY
    settings_pet_shop: Optional[SettingsPetShop] = field(default_factory=lambda: SettingsPetShop())
    settings_food_shop: Optional[SettingsFoodShop] = field(default_factory=lambda: SettingsFoodShop())
