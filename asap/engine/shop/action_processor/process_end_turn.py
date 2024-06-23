import random

from asap.actions import ActionEndTurn
from asap.team.team import Team


def process_end_turn(_: ActionEndTurn, team: Team, game):
    from asap.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]

    team_shop_state.shop.turn += 1
    team_shop_state.money = game.settings.starting_money
    team_shop_state.shop.refresh()

    team.end_turn(team_shop_state)

    game.play_battle_round()
