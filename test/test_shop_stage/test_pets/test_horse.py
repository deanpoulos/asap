from asap.pets import Horse, Duck
from asap.pets.pet import LEVEL_2_EXP, LEVEL_3_EXP


def test_horse_on_friend_summoned(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = game.team_states[team].shop.pet_shop

    team.add_pet(0, Horse())
    team.add_pet(1, Duck())

    # make sure Horse added one attack
    assert team.pets[1].attack == Duck.base_attack + 1

    team.add_pet(2, Horse(exp=LEVEL_2_EXP))

    team.add_pet(3, Duck())

    # make sure first Horse added one attack, second horse added 2
    assert team.pets[2].attack == Duck.base_attack + 1 + 2

    team.add_pet(4, Horse(exp=LEVEL_3_EXP))

    team.remove_pet(1)
    team.add_pet(1, Duck())

    # make sure first Horse added one attack, second horse added 2, third 3
    assert team.pets[1].attack == Duck.base_attack + 1 + 2 + 3

