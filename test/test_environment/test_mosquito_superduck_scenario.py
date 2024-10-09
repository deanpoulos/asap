from sb3_contrib.common.wrappers import ActionMasker

from asap.engine.actions import ActionBuyAndPlacePet, ActionBuyAndMergePet, ActionEndTurn, ActionMergePets, \
    ActionSellPet
from asap.training.environment.action_masker import mask_fn
from asap.training.environment.environment import AsapEnvironmentTwoPlayer
from asap.training.scenarios.mosquito_upgrade_to_superduck_scenario import mosquito_to_superduck_game_settings


def test_mosquito_superduck_scenario_turn_2_upgrade():
    env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings)
    env = ActionMasker(env, action_mask_fn=mask_fn)

    env.reset()

    actions = [
        ActionBuyAndPlacePet(0, 0),
        ActionBuyAndPlacePet(1, 1),
        ActionBuyAndMergePet(2, 0),
        ActionEndTurn(),
        ActionMergePets(1, 0),
        ActionBuyAndPlacePet(0, 1)
    ]
    for action in actions:
        action_mask = mask_fn(env)
        assert action_mask[env.action_map_inverse[action]] == 1
        obs, _, _, _, _ = env.step(env.action_map_inverse[action])


def test_mosquito_superduck_scenario_turn_1_upgrade():
    env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings)
    env = ActionMasker(env, action_mask_fn=mask_fn)

    env.reset()

    actions = [
        ActionBuyAndPlacePet(0, 0),
        ActionBuyAndMergePet(1, 0),
        ActionBuyAndMergePet(2, 0),
        ActionSellPet(0),
        ActionBuyAndPlacePet(0, 0),
        ActionEndTurn(),
    ]
    for action in actions:
        action_mask = mask_fn(env)
        assert action_mask[env.action_map_inverse[action]] == 1
        obs, _, _, _, _ = env.step(env.action_map_inverse[action])
