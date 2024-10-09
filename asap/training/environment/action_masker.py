import numpy as np
import nvtx

from asap.engine.actions import ActionEndTurn

MAX_ACTIONS_PER_TURN = 10


@nvtx.annotate("mask actions")
def mask_fn(env) -> np.ndarray:
    action_mask = np.zeros(len(env.action_map), dtype=int)

    if env.action_index >= MAX_ACTIONS_PER_TURN-1:
        action_mask[env.action_map_inverse[ActionEndTurn()]] = 1
    else:
        for i in range(len(action_mask)):
            action = env.action_map[i]
            if env.game.is_valid_action(action, env.team_left):
                action_mask[i] = 1
        action_mask[env.action_map_inverse[ActionEndTurn()]] = 0
    return action_mask
