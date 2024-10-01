from dataclasses import dataclass, field

from asap.engine.shop.shop import Shop
from asap.engine.team.team import Team


@dataclass
class TeamShopState:
    team: Team
    money: int
    health: int
    shop: Shop = field(default_factory=Shop)
    previous_battle_outcome: int | None = None
    wins: int = 0
