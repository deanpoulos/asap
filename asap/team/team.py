from typing import Dict, Type

from asap.pets import Pet
from asap.team.constants import MAX_TEAM_SIZE


class Team:
    def __init__(self):
        self.pets: Dict[int, Pet] = \
            {i: None for i in range(MAX_TEAM_SIZE)}
        self.health: int = 6
        self.wins: int = 0

    def is_full(self) -> bool:
        return not any([pet is None for pet in self.pets.values()])
