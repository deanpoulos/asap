import gymnasium as gym
from asap.engine.actions import (
    ActionRefreshShop, ActionEndTurn, ActionFreezePet, ActionUnfreezePet, ActionBuyAndPlacePet,
    ActionBuyAndMergePet, ActionSellPet, ActionMergePets, ActionSwapPets, ActionFreezeFood,
    ActionUnfreezeFood, ActionBuyFood
)
from asap.engine.engine.game_settings import GameSettings


def make_action_space(game_settings: GameSettings):
    return gym.spaces.Discrete(len(make_possible_actions(game_settings)))

def make_possible_actions(game_settings: GameSettings):
    return (
        make_fixed_actions_mapping() +
        make_pet_shop_actions(game_settings.settings_pet_shop.MAX_ITEMS) +
        make_food_shop_actions(game_settings.settings_food_shop.MAX_ITEMS) +
        make_team_actions(game_settings.max_team_size) +
        make_team_two_pet_actions(game_settings.max_team_size) +
        make_pet_shop_team_actions(game_settings.settings_pet_shop.MAX_ITEMS, game_settings.max_team_size) +
        make_food_shop_team_actions(game_settings.settings_food_shop.MAX_ITEMS, game_settings.max_team_size)
    )

def make_fixed_actions_mapping():
    return [
        ActionRefreshShop(),
        ActionEndTurn()
    ]

def make_pet_shop_actions(max_pets_in_shop: int):
    return sum([
        [
            ActionFreezePet(i),
            ActionUnfreezePet(i),
        ] for i in range(max_pets_in_shop)
    ], [])

def make_food_shop_actions(max_food_in_shop: int):
    return sum([
        [
            ActionFreezeFood(i),
            ActionUnfreezeFood(i),
        ] for i in range(max_food_in_shop)
    ], [])

def make_team_actions(team_size: int):
    return sum([
        [
            ActionSellPet(i),
        ] for i in range(team_size)
    ], [])

def make_team_two_pet_actions(team_size: int):
    actions = []
    for i in range(team_size):
        for j in range(team_size):
            if i != j:
                actions.append(ActionMergePets(i, j))
                actions.append(ActionSwapPets(i, j))
    return actions

def make_pet_shop_team_actions(max_pets_in_shop: int, team_size: int):
    return sum([
        [
            ActionBuyAndPlacePet(i, j),
            ActionBuyAndMergePet(i, j)
        ] for i in range(max_pets_in_shop) for j in range(team_size)
    ], [])

def make_food_shop_team_actions(max_food_in_shop: int, team_size: int):
    return [ ActionBuyFood(i, j) for i in range(max_food_in_shop) for j in range(team_size) ]
