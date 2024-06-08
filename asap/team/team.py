from typing import Dict, Type

from asap.pets import Pet


class Team:
    def __init__(self, max_team_size: int):
        self.pets: Dict[int, Pet | None] = \
            {i: None for i in range(max_team_size)}
        self.health: int = 6
        self.wins: int = 0

    def is_full(self) -> bool:
        return not any([pet is None for pet in self.pets.values()])

    def remove_pet(self, pet_position: int):
        self.pets[pet_position] = None
