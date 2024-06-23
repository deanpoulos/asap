from typing import Dict

from asap.engine.shop.action_processor._errors import PositionOccupiedError
from asap.pets import Pet


class Team:
    def __init__(self, max_team_size: int):
        self.pets: Dict[int, Pet | None] = \
            {i: None for i in range(max_team_size)}

    def is_full(self) -> bool:
        return not any([pet is None for pet in self.pets.values()])

    def add_pet(self, pet_position: int, pet: Pet):
        if self.pets[pet_position] is not None:
            raise PositionOccupiedError(pet_position)
        if pet_position not in self.pets.keys():
            raise Exception()
        self.pets[pet_position] = pet
        for other_pet in [other_pet for other_pet in self.pets.values() if other_pet is not None and other_pet != pet]:
            other_pet.on_friend_summoned(pet)

    def push_pet(self, pet_position: int, pet: Pet):
        if self.pets[pet_position] is not None:
            pets = {i: self.pets[i] if i < pet_position else None for i in range(len(self.pets))}
            next_empty_space = len(self.pets) - 1
            for i in range(pet_position, len(self.pets)):
                if self.pets[i] is None:
                    next_empty_space = i
                    break
            for i in range(next_empty_space, pet_position, -1):
                pets[i] = self.pets[i - 1]
            self.pets = pets
        self.add_pet(pet_position, pet)

    def remove_pet(self, pet_position: int):
        self.pets[pet_position] = None

    def start_battle(self, state):
        for pet in self.pets.values():
            if pet is not None:
                pet.on_start_battle(state)

    def end_turn(self, state):
        for pet in self.pets.values():
            if pet is not None:
                pet.on_end_turn(state)

    def is_alive(self):
        return any([pet.health > 0 for pet in self.pets.values() if pet is not None])

    def __str__(self):
        return " ".join([f"{pet} " for position, pet in self.pets.items()])
