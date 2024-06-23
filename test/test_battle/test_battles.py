import random

from asap.engine.battle.battle import Battle
from asap.engine.battle.battle_result import TeamBattleResult
from asap.foods.tier1.honey import HoneyPerk
from asap.pets import Duck, Mosquito, Cricket, Horse, Pig, Ant, Otter
from asap.pets.pet import LEVEL_3_EXP, LEVEL_2_EXP


def test_battle_mosquito_cricket_vs_duck_duck(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Mosquito())
    team_l.add_pet(1, Cricket())
    team_r.add_pet(0, Duck())
    team_r.add_pet(1, Duck())

    random.seed(0)
    battle = Battle(team_l, team_r)

    result = battle.play()

    assert result.team_l_result.result == TeamBattleResult.Result.LOSS
    assert result.team_r_result.result == TeamBattleResult.Result.WIN


def test_battle_mosquito_vs_cricket(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Mosquito())
    team_r.add_pet(1, Cricket())

    random.seed(0)
    battle = Battle(team_l, team_r)

    result = battle.play()

    assert result.team_l_result.result == TeamBattleResult.Result.DRAW
    assert result.team_r_result.result == TeamBattleResult.Result.DRAW


def test_battle_horse_cricket_vs_duck_pig(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Cricket())
    team_l.add_pet(1, Horse())
    team_r.add_pet(0, Duck())
    team_r.add_pet(1, Pig())

    random.seed(0)
    battle = Battle(team_l, team_r)

    result = battle.play()

    assert result.team_l_result.result == TeamBattleResult.Result.DRAW
    assert result.team_r_result.result == TeamBattleResult.Result.DRAW


def test_battle_5_mosquitos_vs_4_crickets_1hp_horse(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Cricket(health=1))
    team_l.add_pet(1, Cricket(health=1))
    team_l.add_pet(2, Cricket(health=1))
    team_l.add_pet(3, Cricket(health=1))
    team_l.add_pet(4, Horse(health=2))
    team_r.add_pet(0, Mosquito())
    team_r.add_pet(1, Mosquito())
    team_r.add_pet(2, Mosquito())
    team_r.add_pet(3, Mosquito())
    team_r.add_pet(4, Mosquito())

    # seed s.t. mosquitos only hit horse once
    random.seed(0)
    battle = Battle(team_l, team_r)

    result = battle.play()

    assert result.team_l_result.result == TeamBattleResult.Result.DRAW
    assert result.team_r_result.result == TeamBattleResult.Result.DRAW


def test_battle_lvl3_ant_ant_pig_vs_4_crickets_horse(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Ant(exp=LEVEL_3_EXP))
    team_l.add_pet(1, Ant())
    team_l.add_pet(2, Pig())
    team_r.add_pet(0, Cricket())
    team_r.add_pet(1, Cricket())
    team_r.add_pet(2, Cricket())
    team_r.add_pet(3, Cricket())
    team_r.add_pet(4, Horse())

    # seed s.t. first ant changes other ant's stats
    random.seed(0)
    battle = Battle(team_l, team_r)

    result = battle.play()

    assert result.team_l_result.result == TeamBattleResult.Result.DRAW
    assert result.team_r_result.result == TeamBattleResult.Result.DRAW


def test_battle_honey_cricket_lvl2_horse_otter_vs_lvl3_ant_ant(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    honeyed_cricket = Cricket()
    honeyed_cricket.perk = HoneyPerk()

    team_l.add_pet(0, honeyed_cricket)
    team_l.add_pet(1, Horse(exp=LEVEL_2_EXP))
    team_l.add_pet(2, Otter())
    team_r.add_pet(0, Ant(exp=LEVEL_3_EXP))
    team_r.add_pet(1, Ant())

    random.seed(0)
    battle = Battle(team_l, team_r)

    result = battle.play()

    assert result.team_l_result.result == TeamBattleResult.Result.DRAW
    assert result.team_r_result.result == TeamBattleResult.Result.DRAW

