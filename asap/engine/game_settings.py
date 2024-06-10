from dataclasses import dataclass, field
from typing import Optional

from asap.shop.settings import SettingsPetShop, SettingsFoodShop


DEFAULT_ROLL_PRICE = 1
DEFAULT_STARTING_TURN = 1
DEFAULT_MAX_TEAM_SIZE = 5
DEFAULT_STARTING_TEAM_HEALTH = 6
DEFAULT_MAX_PET_LEVEL = 3


@dataclass
class GameSettings:
    max_team_size: Optional[int] = DEFAULT_MAX_TEAM_SIZE
    starting_team_health: Optional[int] = DEFAULT_STARTING_TEAM_HEALTH
    starting_turn: Optional[int] = DEFAULT_STARTING_TURN
    max_pet_level: Optional[int] = DEFAULT_MAX_PET_LEVEL
    roll_price: Optional[int] = DEFAULT_ROLL_PRICE
    settings_pet_shop: Optional[SettingsPetShop] = field(default_factory=lambda: SettingsPetShop())
    settings_food_shop: Optional[SettingsFoodShop] = field(default_factory=lambda: SettingsFoodShop())