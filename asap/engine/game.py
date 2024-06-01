from typing import List, Dict

from asap.engine.actions import *
from asap.engine.actions.errors import *
from asap.engine.constants import STARTING_TURN
from asap.engine.shop import PetShop
from asap.engine.team import Team, TeamBattleState, TeamShopState
from asap.engine.team.constants import MAX_TEAM_SIZE


class Game:
    def __init__(self, teams: List[Team]):
        self.teams: List[Team] = teams
        self.team_states: Dict[Team, TeamShopState] = {
            team: TeamShopState(team, PetShop()) for team in self.teams
        }
        self.turn = STARTING_TURN

    def battle(self, team_left: Team, team_right: Team):
        while team_left.still_alive() and team_right.still_alive():
           pass

    def get_shop(self, team: Team):
        return self.team_states[team].shop

    def _check_for_winner(self):
        if len(self.teams) == 1:
            return True
        else:
            return False

    def submit_action(self, team: Team, action: Action):
        if isinstance(action, ActionBuyPet):
            team_shop_state = self.team_states[team]
            shop = team_shop_state.shop

            if shop.already_bought(action.shop_index):
                raise AlreadyBoughtError(shop.items[action.shop_index])

            item_price = shop.price(action.shop_index)
            if team_shop_state.money < item_price:
                raise NotEnoughMoneyError(team_shop_state.money, item_price)

            if team.is_full():
                raise TeamFullError()

            if team.pets[action.pet_position] is not None:
                raise PositionOccupiedError(action.pet_position)

            team_shop_state.money -= item_price
            pet = shop.buy(action.shop_index)
            team.pets[action.pet_position] = pet

        elif isinstance(action, ActionRefreshShop):
            team_shop_state = self.team_states[team]
            shop = team_shop_state.shop

            roll_price = shop.roll_price
            if team_shop_state.money < roll_price:
                raise NotEnoughMoneyError(team_shop_state.money, roll_price)

            team_shop_state.money -= roll_price
            shop.refresh(self.turn)

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
