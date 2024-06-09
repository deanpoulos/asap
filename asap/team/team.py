from typing import Dict

from asap.pets import Pet


class Team:
    def __init__(self, max_team_size: int, starting_health: int):
        self.pets: Dict[int, Pet | None] = \
            {i: None for i in range(max_team_size)}
        self.health: int = starting_health
        self.wins: int = 0

    def is_full(self) -> bool:
        return not any([pet is None for pet in self.pets.values()])

    def add_pet(self, pet_position: int, pet: Pet):
        if pet_position not in self.pets.keys():
            raise Exception()
        self.pets[pet_position] = pet

    def remove_pet(self, pet_position: int):
        self.pets[pet_position] = None

    def __str__(self):
        return " ".join([f"{pet} " for position, pet in self.pets.items()])
