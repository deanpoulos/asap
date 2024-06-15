from dataclasses import dataclass, field

from asap.shop.shop import Shop
from asap.team.team import Team


@dataclass
class TeamShopState:
    team: Team
    money: int
    shop: Shop = field(default_factory=Shop)
