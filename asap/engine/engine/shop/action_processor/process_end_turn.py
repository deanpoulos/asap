import random

from asap.engine.actions import ActionEndTurn
from asap.engine.team.team import Team


def process_end_turn(_: ActionEndTurn, team: Team, game):
    from asap.engine.engine.game import Game
    game: Game
    team_shop_state = game.team_states[team]

    team_shop_state.shop.turn += 1
    team_shop_state.money = game.settings.starting_money
    team_shop_state.shop.refresh()

    team.end_turn(team_shop_state)

    game.play_battle_round()
