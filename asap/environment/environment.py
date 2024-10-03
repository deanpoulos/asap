from typing import SupportsFloat, Any, Dict, Type, List, Callable

import gymnasium as gym
from gymnasium.spaces import flatten, Box
from gymnasium.core import ActType, ObsType
from sb3_contrib import MaskablePPO

from asap.engine.actions import ActionEndTurn, Action
from asap.engine.engine.game import Game
from asap.engine.engine.game_settings import GameSettings
from asap.engine.foods import Food
from asap.engine.pets import Pet
from asap.engine.shop.item import PetItem, FoodItem
from asap.environment.action_masker import mask_fn
from asap.environment.action_space import make_possible_actions, make_action_space
from asap.environment.observation_space import make_pet_observation_map, make_food_observation_map, \
    make_flat_observation_space, make_observation_space


class AsapEnvironmentTwoPlayer(gym.Env[Box, int]):

    def __init__(self, game_settings: GameSettings, make_adversary_callback: Callable[[], MaskablePPO]):
        super(AsapEnvironmentTwoPlayer, self).__init__()

        if game_settings.num_teams != 2:
            raise ValueError(f"Expected number of teams to be 2, got {game_settings.num_teams}")

        self.game: Game = None
        self.adversary: MaskablePPO = None
        self.team_left = None
        self.team_right = None

        self.mask_fn = mask_fn

        self.observation_space = make_flat_observation_space(game_settings)
        self._unflattened_observation_space = make_observation_space(game_settings)
        self.action_space = make_action_space(game_settings)

        self.game_settings = game_settings
        self.make_adversary = make_adversary_callback

        self.is_adversary_playing = False
        self.action_index: int = 0

        self.pet_observation_map: Dict[Type[Pet], int] = make_pet_observation_map(game_settings)
        self.food_observation_map: Dict[Type[Food], int] = make_food_observation_map(game_settings)
        self.action_map: List[Action] = make_possible_actions(game_settings)
        self.action_map_inverse: Dict[Action, int] = {action: i for i, action in enumerate(make_possible_actions(game_settings))}

    def step(
            self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:

        terminated = False
        truncated = False
        reward = 0

        if action == self.action_map_inverse[ActionEndTurn()]:
            self.game.execute_action(ActionEndTurn(), self.team_left)
            if not self.is_adversary_playing:
                self.play_adversary_turn()
            self.game.play_battle_round()
        else:
            self.game.execute_action(self.action_map[action], self.team_left)
            self.action_index += 1

        obs = self.make_observation()

        self.game._prune_teams()

        if self.game.has_winner():
            if self.game.is_winner(self.team_left):
                reward = 1
            else:
                reward = -1
            print(reward)
            terminated = True

        return obs, reward, terminated, truncated, {}

    def play_adversary_turn(self):
        self.team_left = self.game.teams[1]
        self.team_right = self.game.teams[0]
        self.is_adversary_playing = True

        observation = self.make_observation()
        action, _ = self.adversary.predict(observation, action_masks=self.mask_fn(self))

        while action != self.action_map_inverse[ActionEndTurn()]:
            observation, _, _, _, _ = self.step(action)
            action, _ = self.adversary.predict(observation, action_masks=self.mask_fn(self))

        self.team_left = self.game.teams[0]
        self.team_right = self.game.teams[1]
        self.is_adversary_playing = False

    def reset(self, *, seed=None, options=None) -> tuple[ObsType, dict[str, Any]]:
        self.game: Game = Game(self.game_settings)
        self.action_index: int = 0
        self.adversary: MaskablePPO = self.make_adversary()
        self.team_left = self.game.teams[0]
        self.team_right = self.game.teams[1]

        return self.make_observation(), {}


    def make_observation(self) -> dict:
        team_left_state = self.game.team_states[self.team_left]
        team_right_last_state = self.game.last_team_states[self.team_right]

        obs = {
            "team_left": {
                "pets": [self._make_pet_observation(pet) for pet in team_left_state.team.pets.values()],
                "health": team_left_state.health,
            },
            "team_right": {
                "pets": [self._make_pet_observation(pet) for pet in team_right_last_state.team.pets.values()],
                "health": team_right_last_state.health,
            },
            "pet_shop": [
                self._make_pet_item_observation(
                    team_left_state.shop.pet_shop._items.get(i, None)
                )
                for i in range(self.game_settings.settings_pet_shop.MAX_ITEMS)
            ],
            "food_shop": [
                self._make_food_item_observation(
                    team_left_state.shop.food_shop._items.get(i, None)
                )
                for i in range(self.game_settings.settings_food_shop.MAX_ITEMS)
            ],
            "money": team_left_state.money,
            "turn": team_left_state.shop.turn,
        }

        obs = flatten(self._unflattened_observation_space, obs)

        return obs

    def _make_food_observation(self, food: Food) -> int:
        if food is not None:
            return self.food_observation_map[type(food)]
        else:
            return 0


    def _make_pet_observation(self, pet: Pet) -> list[int]:
        if pet is not None:
            return [[pet.attack, pet.health, pet.exp, pet.level], self.pet_observation_map[type(pet)]]
        else:
            return [[0, 0, 0, 0], 0]

    def _make_pet_item_observation(self, item):
        if item is not None:
            return {
                "pet": self._make_pet_observation(item.item),
                "price": item.price
            }
        else:
            return {
                "pet": self._make_pet_observation(None),
                "price": 0
            }

    def _make_food_item_observation(self, item):
        if item is not None:
            return {
                "food": self._make_food_observation(item.item),
                "price": item.price
            }
        else:
            return {
                "food": self._make_food_observation(None),
                "price": 0
            }
