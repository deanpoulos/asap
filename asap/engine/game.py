from typing import List, Dict

from asap.actions import *
from asap.engine.action_processor.process_buy_pet import process_buy_pet
from asap.engine.action_processor.process_freeze_pet import process_freeze_pet
from asap.engine.action_processor.process_refresh_shop import process_refresh_shop
from asap.engine.constants import STARTING_TURN
from asap.shop import PetShop
from asap.team import Team, TeamBattleState, TeamShopState
from asap.team.constants import MAX_TEAM_SIZE


class Game:
    def __init__(self, teams: List[Team]):
        self.turn = STARTING_TURN
        self.teams: List[Team] = teams
        self.team_states: Dict[Team, TeamShopState] = {
            team: TeamShopState(team, PetShop()) for team in self.teams
        }
        for team_shop_state in self.team_states.values():
            team_shop_state.pet_shop.refresh(self.turn)

    def battle(self, team_left: Team, team_right: Team):
        while team_left.still_alive() and team_right.still_alive():
           pass

    def get_shop(self, team: Team):
        return self.team_states[team].pet_shop

    def _check_for_winner(self):
        if len(self.teams) == 1:
            return True
        else:
            return False

    def execute_action(self, action: Action, team: Team):
        if isinstance(action, ActionBuyPet):
            process_buy_pet(action, team, self)

        elif isinstance(action, ActionRefreshShop):
            process_refresh_shop(action, team, self)

        elif isinstance(action, ActionFreezePet):
            process_freeze_pet(action, team, self)

        else:
            raise NotImplementedError()

    # def allowed_actions(self, team: Team):
    #     not_allowed_actions = []
    #     team_shop_state = self.team_states[team]
    #     if len(team.pets) == 5:
    #         not_allowed_actions.append(ActionBuyPet)
    #     if len(team.pets) == 0:
    #         not_allowed_actions.append(ActionSellPet)
    #     if team_shop_state.money == 0
    #         not_allowed_actions.append(ActionSellPet)
    #         not_allowed_actions.append(ActionSellPet)
