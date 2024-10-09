from pathlib import Path

import numpy as np
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from asap.engine.actions import ActionEndTurn
from asap.training.environment.environment import AsapEnvironmentTwoPlayer
from asap.training.opponents.self_play.adversary_loader import OpponentLoaderBest
from asap.training.opponents.self_play.adversary_self_play import OpponentSelfPlay
from asap.training.scenarios.mosquito_upgrade_to_superduck_scenario.settings import mosquito_to_superduck_game_settings


def test_selfplay_reward():
    load_dir = Path('/home/dean/src/asap/training/runs/2024-10-10/02-54-21')
    eval_opponent_loader = OpponentLoaderBest(MaskablePPO, load_dir)
    eval_opponent = OpponentSelfPlay(loader=eval_opponent_loader)
    eval_env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings, eval_opponent,
                                        observe_opponent_after_battle=False, use_flat_observations=True, verbose=1)
    eval_env = ActionMasker(eval_env, eval_env.mask_fn)

    agent = MaskablePPO.load(load_dir / "best_model.zip")

    rewards = []
    for _ in range(100):
        eval_env.reset()
        action = None
        observation = eval_env.make_observation()
        while action != eval_env.action_map_inverse[ActionEndTurn()]:
            action, _ = agent.predict(observation, deterministic=True, action_masks=eval_env.mask_fn(eval_env))
            observation, reward, _, _, _ = eval_env.step(action)
            rewards.append(reward)

    print(rewards)
    assert np.mean(rewards) < 0.1
