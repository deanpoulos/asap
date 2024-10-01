from asap.engine.engine.battle.battle import Battle
from asap.engine.pets import Duck
from asap.engine.pets.pet import MAX_ATTACK, MAX_HEALTH


def test_pet_prioritization(game_turn_1_2_teams):
    game = game_turn_1_2_teams

    team_l = game.teams[0]
    team_r = game.teams[1]

    team_l.add_pet(0, Duck())
    team_l.add_pet(1, Duck(exp=1))
    team_l.add_pet(2, Duck(exp=1, health=MAX_HEALTH))

    team_r.add_pet(0, Duck())
    team_r.add_pet(1, Duck(exp=2))
    team_r.add_pet(2, Duck(exp=2))
    team_r.add_pet(3, Duck(exp=2, health=MAX_HEALTH))
    team_r.add_pet(4, Duck(exp=2, attack=MAX_ATTACK, health=1))

    battle = Battle(team_l, team_r)

    battle.assign_pet_priorities()

    assert len(battle.pets_in_priority_order) == 8

    # check that pet priorities are in descending order of attack, then health
    most_recent_attack = MAX_ATTACK
    most_recent_health = MAX_HEALTH
    for pet in battle.pets_in_priority_order:
        assert pet.attack <= most_recent_attack
        if pet.attack == most_recent_attack:
            assert pet.health <= most_recent_health
        most_recent_attack = pet.attack
        most_recent_health = pet.health
