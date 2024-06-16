import logging
import sys

from typing import List, Dict, Optional

from asap.actions import *
from asap.engine.shop.action_processor.process_buy_food import process_buy_food
from asap.engine.shop.action_processor.process_buy_and_place_pet import process_buy_and_place_pet
from asap.engine.shop.action_processor.process_buy_and_merge_pet import process_buy_and_merge_pet
from asap.engine.shop.action_processor.process_end_turn import process_end_turn
from asap.engine.shop.action_processor.process_freeze_food import process_freeze_food
from asap.engine.shop.action_processor.process_freeze_pet import process_freeze_pet
from asap.engine.shop.action_processor.process_merge_pets import process_merge_pets
from asap.engine.shop.action_processor.process_refresh_shop import process_refresh_shop
from asap.engine.shop.action_processor.process_sell_pet import process_sell_pet
from asap.engine.shop.action_processor.process_swap_pets import process_swap_pets
from asap.engine.shop.action_processor.process_unfreeze_food import process_unfreeze_food
from asap.engine.shop.action_processor.process_unfreeze_pet import process_unfreeze_pet
from asap.engine.shop.action_validator.validate_refresh_shop import validate_refresh_shop
from asap.engine.game_settings import GameSettings
from asap.shop.shop import Shop
from asap.team.states import TeamShopState
from asap.team.team import Team

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Game:
    def __init__(self, num_teams: int, settings: Optional[GameSettings] = None):
        if settings is None:
            settings = GameSettings()
        self.settings = settings
        self.teams: List[Team] = []

        for _ in range(num_teams):
            self.teams.append(Team(settings.max_team_size, settings.starting_team_health))
        self.team_states: Dict[Team, TeamShopState] = {}

        for team in self.teams:
            shop = Shop(
                settings_pet_shop=settings.settings_pet_shop,
                settings_food_shop=settings.settings_food_shop,
                roll_price=settings.roll_price,
                turn=self.settings.starting_turn
            )
            self.team_states[team] = TeamShopState(team, settings.starting_money, shop)
            shop.refresh()

    def _check_for_winner(self):
        if len(self.teams) == 1:
            return True
        else:
            return False

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

        # logging.debug(f"\nTEAM: {team}\nSHOP: {self.team_states[team].shop}")

    #
    # def allowed_actions(self, team: Team):
    #     action_space: Dict[Action, bool] = {}
    #
    #     team_shop_state = self.team_states[team]
    #     pet_shop_settings = self.settings.settings_pet_shop
    #
    #     # actions with no input
    #     action_space[ActionRefreshShop()] = validate_refresh_shop(team_shop_state, team)
    #
    #     # actions parameterized by pet shop index input
    #     shop_index_space = (pet_shop_settings.TIER_6_PET_SHOP_SIZE +
    #                         pet_shop_settings.NUM_HIGHER_TIER_UNLOCKS*3)
    #
    #     for shop_index in range(shop_index_space):
    #         action_space[ActionFreezePet(shop_index)] = validate_freeze_pet
