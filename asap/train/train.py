import gymnasium as gym
import numpy as np

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

from asap.engine.engine.game_settings import GameSettings
from asap.environment.action_masker import mask_fn
from asap.environment.environment import AsapEnvironmentTwoPlayer

game_settings = GameSettings(num_teams=2)
env = AsapEnvironmentTwoPlayer(game_settings)  # Initialize env
env = ActionMasker(env, mask_fn)  # Wrap to enable masking

model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1)
model.learn(total_timesteps=100_000)
