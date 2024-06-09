from asap.actions import ActionSellPet
from asap.pets import Duck


def test_duck_on_sell(game_turn_1_ducks_only_apples_only_single_team):
    game = game_turn_1_ducks_only_apples_only_single_team
    team = game.teams[0]
    shop = game.team_states[team].shop.pet_shop

    attacks, healths = dict(), dict()
    for i, pet_item in enumerate(shop._items.values()):
        attacks[i] = pet_item.item.attack
        healths[i] = pet_item.item.health

    team.add_pet(0, Duck())
    game.execute_action(ActionSellPet(0), team)

    # make sure selling duck increased all shop items' healths
    for i, pet_item in enumerate(shop.items.values()):
        assert pet_item.item.attack == attacks[i]
        assert pet_item.item.health == healths[i] + 1
