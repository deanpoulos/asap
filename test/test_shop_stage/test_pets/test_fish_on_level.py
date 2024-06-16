from asap.actions import ActionMergePets
from asap.pets import Duck, Fish


def test_fish_on_level(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]

    team.add_pet(0, Fish())
    team.add_pet(1, Fish())
    team.add_pet(2, Fish())
    team.add_pet(3, Duck())

    game.execute_action(ActionMergePets(2, 1), team)
    game.execute_action(ActionMergePets(1, 0), team)

    assert team.pets[0].level == 2
    assert team.pets[0].exp == 2
    assert team.pets[0].extra_attack == 0
    assert team.pets[0].extra_health == 0

    # other pet gains +1/+1 on fish level up
    assert team.pets[3].extra_attack == 1
    assert team.pets[3].extra_health == 1

    team.add_pet(1, Fish())
    team.add_pet(2, Fish())
    team.add_pet(4, Fish())

    game.execute_action(ActionMergePets(4, 0), team)
    game.execute_action(ActionMergePets(2, 0), team)
    game.execute_action(ActionMergePets(1, 0), team)

    assert team.pets[0].level == 3
    assert team.pets[0].exp == 5
    assert team.pets[0].extra_attack == 0
    assert team.pets[0].extra_health == 0

    # other pet gains additional +2/+2 on fish level up
    assert team.pets[3].extra_attack == 3
    assert team.pets[3].extra_health == 3
