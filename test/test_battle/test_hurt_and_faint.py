from asap.engine.battle.battle import Battle
from asap.pets import Duck, Mosquito
from asap.pets.pet import MAX_ATTACK, MAX_HEALTH


def test_hurt_and_faint(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Mosquito())
    team_r.add_pet(0, Duck(health=1))

    battle = Battle(team_l, team_r)

    battle.assign_pet_priorities()
    battle.phase_start_of_turn()

    # check that the duck has lost one health and is still in team
    assert battle.team_r.pets[0].health == 0

    battle.phase_trigger_on_hurt_and_faint()

    # check that the duck has fainted and is no longer in team
    assert battle.team_r.pets[0] is None
