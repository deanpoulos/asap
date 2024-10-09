from typing import SupportsFloat, Any, Dict, Type, List, Callable

import gymnasium as gym
from gymnasium.spaces import flatten_space
from gymnasium.spaces import flatten
from gymnasium.core import ActType
from nvtx import nvtx

from asap.engine.actions import ActionEndTurn, Action
from asap.engine.engine.battle.battle_result import TeamBattleResult
from asap.engine.engine.game import Game
from asap.engine.engine.game_settings import GameSettings
from asap.engine.foods import Food
from asap.engine.perks import Perk
from asap.engine.pets import Pet
from asap.engine.team.team import Team

from asap.training.opponents.opponent import Opponent
from asap.training.environment.action_masker import mask_fn
from asap.training.environment.action_space import (
    make_possible_actions, make_action_space, make_possible_actions_inverse_mapping
)
from asap.training.environment.observation_space import (
    make_pet_observation_map, make_food_observation_map, make_observation_space,
    make_perk_observation_map, make_flat_observation_space
)


class AsapEnvironmentTwoPlayer(gym.Env[dict, int]):
    def __init__(self,
                 game_settings: GameSettings,
                 opponent: Opponent,
                 post_battle_callback: Callable[[gym.Env], None] = None,
                 use_flat_observations: bool = False,
                 observe_opponent_after_battle: bool = False,
                 verbose=1
                 ):
        super(AsapEnvironmentTwoPlayer, self).__init__()

        if game_settings.num_teams != 2:
            raise ValueError(f"Expected number of teams to be 2, got {game_settings.num_teams}")

        self.game_settings = game_settings
        self.opponent = opponent
        self.post_battle_callback = post_battle_callback
        self.verbose = verbose
        self.use_flat_observations = use_flat_observations
        self.observe_opponent_after_battle = observe_opponent_after_battle

        self.game: Game = None
        self.team_left: Team = None
        self.team_right: Team= None
        self.is_adversary_playing = False
        self.action_index: int = 0

        self.mask_fn = mask_fn

        self.observation_space = make_flat_observation_space(game_settings, observe_opponent_after_battle)
        if self.use_flat_observations:
            self._unflattened_observation_space = self.observation_space
            self.observation_space = flatten_space(self.observation_space)
        self.nested_observation_space = make_observation_space(game_settings, observe_opponent_after_battle)
        self.action_space = make_action_space(game_settings)

        self.pet_observation_map: Dict[Type[Pet], int] = make_pet_observation_map(game_settings)
        self.perk_observation_map: Dict[Type[Perk], int] = make_perk_observation_map(game_settings)
        self.food_observation_map: Dict[Type[Food], int] = make_food_observation_map(game_settings)
        self.action_map: List[Action] = make_possible_actions(game_settings)
        self.action_map_inverse: Dict[Action, int] = make_possible_actions_inverse_mapping(game_settings)

    def step(self, action: ActType) -> tuple[dict, SupportsFloat, bool, bool, dict[str, Any]]:
        terminated = False
        truncated = False
        reward = 0

        if action == self.action_map_inverse[ActionEndTurn()]:
            with nvtx.annotate("Env/ExecuteAction"):
                self.game.execute_action(ActionEndTurn(), self.team_left)
            self.action_index = 0
            if not self.is_adversary_playing:
                if self.opponent is not None:
                    self.play_opponent_turn()
                with nvtx.annotate("Env/Battle"):
                    results = self.game.play_battle_round()
                if results[0].team_l_result.result == TeamBattleResult.Result.WIN:
                    if results[0].team_l_result.team == self.team_left:
                        reward = 1
                    else:
                        reward = -1
                elif results[0].team_l_result.result == TeamBattleResult.Result.LOSS:
                    if results[0].team_l_result.team == self.team_left:
                        reward = -1
                    else:
                        reward = 1
                if self.post_battle_callback is not None:
                    self.post_battle_callback(self)
                if self.verbose > 0:
                    print(self.game)
        else:
            with nvtx.annotate("Env/ExecuteAction"):
                self.game.execute_action(self.action_map[action], self.team_left)

        self.action_index += 1

        obs = self.make_observation()

        if action == self.action_map_inverse[ActionEndTurn()] and not self.is_adversary_playing:
            self.game._prune_teams()

            if self.game.is_over():
                terminated = True
                # if self.game.is_winner(self.team_left):
                #     reward = 1
                # elif self.game.is_winner(self.team_right):
                #     reward = -1

        return obs, reward, terminated, truncated, {}

    @nvtx.annotate("Env/OpponentTurn")
    def play_opponent_turn(self):
        self.team_left = self.game.teams[1]
        self.team_right = self.game.teams[0]
        self.is_adversary_playing = True
        self.action_index = 0

        action = None
        observation = self.make_observation()
        while action != self.action_map_inverse[ActionEndTurn()]:
            action, _ = self.opponent.make_action(observation, action_mask=self.mask_fn(self))
            observation, _, _, _, _ = self.step(action)

        self.team_left = self.game.teams[0]
        self.team_right = self.game.teams[1]
        self.is_adversary_playing = False

    @nvtx.annotate("Env/Reset")
    def reset(self, *, seed=None, options=None) -> tuple[dict, dict[str, Any]]:
        self.game: Game = Game(self.game_settings)
        self.action_index: int = 0
        self.opponent.initialize()
        self.team_left = self.game.teams[0]
        self.team_right = self.game.teams[1]

        return self.make_observation(), {}


    @nvtx.annotate("Env/Observe")
    def make_observation(self) -> dict:
        team_left_state = self.game.team_states[self.team_left]
        team_right_last_state = self.game.last_team_states[self.team_right]

        obs = {
            f"team_left_health": [team_left_state.health],
            f"team_right_health": [team_right_last_state.health],
            **{f"team_left_pet_{i}":
                   flatten(self.nested_observation_space[f"team_left_pet_{i}"], self._make_pet_observation(pet))
                   for i, pet in enumerate(team_left_state.team.pets.values())
               },
            **{f"pet_shop_{i}": flatten(
                self.nested_observation_space[f"pet_shop_{i}"],
                self._make_pet_item_observation(team_left_state.shop.pet_shop._items.get(i, None))
            ) for i in range(self.game_settings.settings_pet_shop.MAX_ITEMS)},
            **{f"food_shop_{i}": flatten(
                self.nested_observation_space.spaces[f"food_shop_{i}"],
                self._make_food_item_observation(team_left_state.shop.food_shop._items.get(i, None))
            ) for i in range(self.game_settings.settings_food_shop.MAX_ITEMS)},
            "money": [team_left_state.money],
            "turn": [team_left_state.shop.turn],
            "action_index": [self.action_index]
        }
        if self.observe_opponent_after_battle:
            obs.update({f"team_right_pet_{i}":
                   flatten(self.nested_observation_space[f"team_right_pet_{i}"], self._make_pet_observation(pet))
               for i, pet in enumerate(team_right_last_state.team.pets.values())
               }
            )

        if self.use_flat_observations:
            obs = flatten(self._unflattened_observation_space, obs)

        return obs

    def _make_food_observation(self, food: Food | None) -> int:
        if food is not None:
            return self.food_observation_map[type(food)]
        else:
            return 0


    def _make_pet_observation(self, pet: Pet | None) -> list[int]:
        if pet is not None:
            return [[pet.attack, pet.health, pet.exp, pet.level],
                    self.pet_observation_map[type(pet)], self.perk_observation_map[type(pet.perk)]]
        else:
            return [[0, 0, 0, 0], self.pet_observation_map[type(pet)], 0]

    def _make_pet_item_observation(self, item):
        if item is not None:
            return [self._make_pet_observation(item.item), item.price]
        else:
            return [self._make_pet_observation(None), 0]

    def _make_food_item_observation(self, item):
        if item is not None:
            return [self._make_food_observation(item.item), item.price]
        else:
            return [self._make_food_observation(None), 0]
