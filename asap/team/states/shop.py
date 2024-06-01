from dataclasses import dataclass, field

from asap.engine.shop import PetShop
from asap.engine.team.team import Team


STARTING_MONEY = 10


@dataclass
class TeamShopState:
    team: Team
    shop: PetShop = field(default_factory=PetShop)
    money: int = STARTING_MONEY
