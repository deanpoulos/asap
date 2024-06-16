from asap.engine.battle.battle import Battle
from asap.pets import Duck, Mosquito
from asap.pets.pet import MAX_ATTACK, MAX_HEALTH


def test_start_of_battle(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Mosquito())
    team_r.add_pet(0, Duck())

    battle = Battle(team_l, team_r)

    battle.assign_pet_priorities()
    battle.start_of_turn()

    # check that the duck has lost one health
    assert battle.team_r.pets[0].health == Duck.base_health - 1

    for _ in range(MAX_HEALTH - 1):
        battle.start_of_turn()

    # check that the duck is not targeted if it is 0 or lower
    assert battle.team_r.pets[0].health == 0

