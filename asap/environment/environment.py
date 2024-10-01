from typing import SupportsFloat, Any, Dict, Type

import gymnasium as gym
from gymnasium.core import ActType, ObsType

from asap.engine.actions import ActionEndTurn
from asap.engine.engine.game import Game
from asap.engine.engine.game_settings import GameSettings
from asap.engine.foods import Food
from asap.engine.pets import Pet
from asap.environment.observation_space import make_pet_observation_map, make_food_observation_map

MAX_ACTIONS_BEFORE_TRUNCATION = 30

class AsapEnvironmentTwoPlayer(gym.Env[dict, int]):
    def __init__(self, game_settings: GameSettings):
        if game_settings.num_teams != 2:
            raise ValueError(f"Expected number of teams to be 2, got {game_settings.num_teams}")
        self.game: Game = Game(game_settings)
        self.team_left = self.game.teams[0]
        self.team_right = self.game.teams[1]
        self.action_index: int = 0
        self._pet_observation_map: Dict[Type[Pet], int] = make_pet_observation_map(game_settings)
        self._food_observation_map: Dict[Type[Food], int] = make_food_observation_map(game_settings)

    def step(
            self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:

        terminated = False
        truncated = False
        reward = 0

        if isinstance(action, ActionEndTurn):
            terminated = True
        elif self.action_index >= MAX_ACTIONS_BEFORE_TRUNCATION:
            truncated = True

        if truncated or terminated:
            self.game.execute_action(ActionEndTurn(), self.team_left)
        else:
            self.game.execute_action(action, self.team_left)
            self.action_index += 1

        obs = self._make_observation()

        if self.game.has_winner():
            if self.game.is_winner(self.team_left):
                reward = 1
            else:
                reward = -1

        return obs, reward, terminated, truncated, {}


    def reset(self, *, seed=None, options=None) -> tuple[ObsType, dict[str, Any]]:
        self.action_index = 0
        return self._make_observation()


    def _make_observation(self) -> dict:
        team_left_state = self.game.team_states[self.team_left]
        team_right_last_state = self.game.last_team_states[self.team_right]

        # todo: map food to category
        obs = {
            "team_left": {
                "pets": [self._make_pet_observation(pet) for pet in team_left_state.team.pets.values()],
                "health": team_left_state.health,
            },
            "team_right_last_state": {
                "pets": [self._make_pet_observation(pet) for pet in team_right_last_state.team.pets.values()],
                "health": team_right_last_state.health,
            },
            "pet_shop": [
                [self._make_pet_observation(item.item), item.price]
                for item in team_left_state.shop.pet_shop.items.values()
            ],
            "food_shop": [
                [self._make_food_observation(item.item), item.price]
                for item in team_left_state.shop.food_shop.items.values()
            ],
            "money": team_left_state.money,
            "turn": team_left_state.shop.turn,
        }

        return obs

    def _make_food_observation(self, food: Food) -> int:
        if food is not None:
            return self._food_observation_map[type(food)]
        else:
            return 0


    def _make_pet_observation(self, pet: Pet) -> list[int]:
        if pet is not None:
            return [pet.attack, pet.health, pet.exp, pet.level, self._pet_observation_map[type(pet)]]
        else:
            return [0, 0, 0, 0, 0]
