import numpy as np

from asap.environment.environment import AsapEnvironmentTwoPlayer


def mask_fn(env: AsapEnvironmentTwoPlayer) -> np.ndarray:
    action_mask = np.zeros(len(env.action_map), dtype=int)
    for i in range(len(action_mask)):
        action = env.action_map[i]
        if env.game.is_valid_action(action, env.team_left):
            action_mask[i] = 1

    return action_mask
