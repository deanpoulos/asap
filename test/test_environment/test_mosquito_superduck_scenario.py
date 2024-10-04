from sb3_contrib.common.wrappers import ActionMasker

from asap.engine.actions import ActionBuyAndPlacePet, ActionBuyAndMergePet, ActionEndTurn, ActionMergePets
from asap.engine.engine.game_settings import GameSettings
from asap.engine.pets import Mosquito, Duck
from asap.engine.shop.settings import SettingsPetShop, SettingsFoodShop
from asap.training.environment.action_masker import mask_fn
from asap.training.environment.environment import AsapEnvironmentTwoPlayer


def test_mosquito_superduck_scenario():
    class SuperDuck(Duck):
        base_attack = 10
        base_health = 10

        def __init__(self):
            super().__init__(attack=self.base_attack, health=self.base_health)

    game_settings = GameSettings(
        num_teams=2,
        starting_team_health=2,
        max_turn=2,
        settings_pet_shop=SettingsPetShop(
            TIER_1_PETS=[Mosquito],
            TIER_2_PETS=[SuperDuck],
            TIER_3_PETS=[Mosquito],
            MAX_ITEMS=5
        ),
        settings_food_shop=SettingsFoodShop(
            MAX_ITEMS=3
        ),
        max_team_size=2
    )

    env = AsapEnvironmentTwoPlayer(game_settings)
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
