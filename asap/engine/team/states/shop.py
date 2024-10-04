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

    def __str__(self):
        return f"{self.team}\n" \
               f"Money: {self.money}\n" \
               f"Health: {self.health}\n" \
               f"Shop: {self.shop}\n" \
               f"Previous Battle Outcome: {self.previous_battle_outcome}\n" \
               f"Wins: {self.wins}"