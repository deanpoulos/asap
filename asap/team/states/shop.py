from dataclasses import dataclass, field

from asap.shop.shop import Shop
from asap.team.team import Team


STARTING_MONEY = 10


@dataclass
class TeamShopState:
    team: Team
    shop: Shop = field(default_factory=Shop)
    money: int = STARTING_MONEY
