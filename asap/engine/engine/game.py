import copy
import logging
import random
import sys

from typing import List, Dict, Optional

from asap.engine.actions import *
from asap.engine.engine.battle.battle import Battle
from asap.engine.engine.battle.battle_result import WIN, LOSS, BattleResult
from asap.engine.engine.shop.action_processor.process_buy_food import process_buy_food
from asap.engine.engine.shop.action_processor.process_buy_and_place_pet import process_buy_and_place_pet
from asap.engine.engine.shop.action_processor.process_buy_and_merge_pet import process_buy_and_merge_pet
from asap.engine.engine.shop.action_processor.process_end_turn import process_end_turn
from asap.engine.engine.shop.action_processor.process_freeze_food import process_freeze_food
from asap.engine.engine.shop.action_processor.process_freeze_pet import process_freeze_pet
from asap.engine.engine.shop.action_processor.process_merge_pets import process_merge_pets
from asap.engine.engine.shop.action_processor.process_refresh_shop import process_refresh_shop
from asap.engine.engine.shop.action_processor.process_sell_pet import process_sell_pet
from asap.engine.engine.shop.action_processor.process_swap_pets import process_swap_pets
from asap.engine.engine.shop.action_processor.process_unfreeze_food import process_unfreeze_food
from asap.engine.engine.shop.action_processor.process_unfreeze_pet import process_unfreeze_pet
# from asap.engine.engine.shop.action_validator.validate_refresh_shop import validate_refresh_shop
from asap.engine.engine.game_settings import GameSettings
from asap.engine.engine.shop.action_validator.validate_buy_and_merge_pet import validate_buy_and_merge_pet
from asap.engine.engine.shop.action_validator.validate_buy_and_place_pet import validate_buy_and_place_pet
from asap.engine.engine.shop.action_validator.validate_buy_food import validate_buy_food
from asap.engine.engine.shop.action_validator.validate_freeze_food import validate_freeze_food
from asap.engine.engine.shop.action_validator.validate_freeze_pet import validate_freeze_pet
from asap.engine.engine.shop.action_validator.validate_merge_pets import validate_merge_pets
from asap.engine.engine.shop.action_validator.validate_refresh_shop import validate_refresh_shop
from asap.engine.engine.shop.action_validator.validate_sell_pet import validate_sell_pet
from asap.engine.engine.shop.action_validator.validate_swap_pets import validate_swap_pets
from asap.engine.engine.shop.action_validator.validate_unfreeze_food import validate_unfreeze_food
from asap.engine.engine.shop.action_validator.validate_unfreeze_pet import validate_unfreeze_pet
from asap.engine.shop.shop import Shop
from asap.engine.team.states import TeamShopState
from asap.engine.team.team import Team

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Game:
    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.teams: List[Team] = []

        for _ in range(settings.num_teams):
            self.teams.append(Team(settings.max_team_size))
        self.team_states: Dict[Team, TeamShopState] = {}
        self.last_team_states: Dict[Team, TeamShopState] = {}

        for team in self.teams:
            shop = Shop(
                settings_pet_shop=settings.settings_pet_shop,
                settings_food_shop=settings.settings_food_shop,
                roll_price=settings.roll_price,
                turn=self.settings.starting_turn
            )
            self.team_states[team] = TeamShopState(
                team, settings.starting_money, settings.starting_team_health, shop=shop
            )
            shop.refresh()

        self.capture_last_team_states()

    def capture_last_team_states(self):
        for team in self.team_states:
            self.last_team_states[team] = copy.deepcopy(self.team_states[team])

    def execute_action(self, action: Action, team: Team):
        if isinstance(action, ActionBuyAndPlacePet):
            process_buy_and_place_pet(action, team, self)
        elif isinstance(action, ActionBuyFood):
            process_buy_food(action, team, self)
        elif isinstance(action, ActionRefreshShop):
            process_refresh_shop(action, team, self)
        elif isinstance(action, ActionFreezeFood):
            process_freeze_food(action, team, self)
        elif isinstance(action, ActionFreezePet):
            process_freeze_pet(action, team, self)
        elif isinstance(action, ActionUnfreezeFood):
            process_unfreeze_food(action, team, self)
        elif isinstance(action, ActionUnfreezePet):
            process_unfreeze_pet(action, team, self)
        elif isinstance(action, ActionSellPet):
            process_sell_pet(action, team, self)
        elif isinstance(action, ActionMergePets):
            process_merge_pets(action, team, self)
        elif isinstance(action, ActionBuyAndMergePet):
            process_buy_and_merge_pet(action, team, self)
        elif isinstance(action, ActionSwapPets):
            process_swap_pets(action, team, self)
        elif isinstance(action, ActionEndTurn):
            process_end_turn(action, team, self)
        else:
            raise NotImplementedError()

    def is_valid_action(self, action: Action, team: Team) -> bool:
        if isinstance(action, ActionBuyAndPlacePet):
            return validate_buy_and_place_pet(action, self.team_states[team])
        elif isinstance(action, ActionBuyFood):
            return validate_buy_food(action, self.team_states[team])
        elif isinstance(action, ActionRefreshShop):
            return validate_refresh_shop(action, self.team_states[team])
        elif isinstance(action, ActionFreezeFood):
            return validate_freeze_food(action, self.team_states[team])
        elif isinstance(action, ActionFreezePet):
            return validate_freeze_pet(action, self.team_states[team])
        elif isinstance(action, ActionUnfreezeFood):
            return validate_unfreeze_food(action, self.team_states[team])
        elif isinstance(action, ActionUnfreezePet):
            return validate_unfreeze_pet(action, self.team_states[team])
        elif isinstance(action, ActionSellPet):
            return validate_sell_pet(action, self.team_states[team])
        elif isinstance(action, ActionMergePets):
            return validate_merge_pets(action, self.team_states[team], self.settings.max_pet_level)
        elif isinstance(action, ActionBuyAndMergePet):
            return validate_buy_and_merge_pet(action, self.team_states[team], self.settings.max_pet_level)
        elif isinstance(action, ActionSwapPets):
            return validate_swap_pets(action, self.team_states[team])
        elif isinstance(action, ActionEndTurn):
            return True
        else:
            raise NotImplementedError()


    def play_battle_round(self) -> List[BattleResult]:
        pairings = self._make_pairings()
        all_results = []
        for pairing in pairings:
            battle = Battle(*pairing)
            results = battle.play()
            all_results.append(results)
            for result in results:
                if result.result == WIN:
                    self.team_states[result.team].wins += 1
                if result.result == LOSS:
                    self.team_states[result.team].health -= 1
                self.team_states[result.team].previous_battle_outcome = result.result
            self.capture_last_team_states()

        return all_results

    def _make_pairings(self):
        teams = self.teams[:]
        random.shuffle(teams)

        if len(teams) % 2 == 1:
            teams.append(teams[0])

        return [teams[i:i + 2] for i in range(0, len(teams), 2)]


    def is_over(self):
        return self.reached_turn_limit() or self.one_team_left()

    def reached_turn_limit(self):
        return any([self.team_states[self.teams[i]].shop.turn > self.settings.max_turn for i in range(len(self.teams))])

    def one_team_left(self):
        if len(self.teams) == 1:
            return True
        else:
            return False

    def is_winner(self, team: Team) -> bool:
        if self.one_team_left():
            if team in self.teams:
                return True
            else:
                return False

        is_exclusively_healthiest_team_at_turn_limit = all(
            [self.team_states[team].health > self.team_states[other_team].health
             for other_team in self.teams if other_team != team])

        if is_exclusively_healthiest_team_at_turn_limit:
            return True

    def _prune_teams(self):
        for team in self.teams:
            team_state = self.team_states[team]
            if team_state.health <= 0:
                self.teams.remove(team)
                self.team_states.pop(team)

    def __str__(self):
        s = ""
        for team in self.teams:
            s += f"Team {team}\n"
            # s += str(self.team_states[team])
            # s += f"\n"

        return s
