import numpy as np
import torch
from matplotlib import pyplot as plt
from torch import nn
from torchviz import make_dot

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker

from asap.training.environment.environment import AsapEnvironmentTwoPlayer
from asap.training.scenarios.mosquito_upgrade_to_superduck_scenario.optimal_adversary import \
    OpponentOptimalMosquitoUpgradeToSuperduckScenario
from asap.training.scenarios.mosquito_upgrade_to_superduck_scenario.settings import mosquito_to_superduck_game_settings

# Load or create your Maskable PPO model
model = MaskablePPO.load("/home/dean/src/asap/training/runs/2024-10-08/02-24-27/3000_model", device='cpu')
# Extract policy network
policy_model = model.policy

# Sample some observations from the environment
opponent = OpponentOptimalMosquitoUpgradeToSuperduckScenario({})
env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings, opponent, use_flat_observations=True, observe_opponent_after_battle=False, verbose=0)
env = ActionMasker(env, env.mask_fn)

opponent.action_map_inverse = env.action_map_inverse

obs, _  = env.reset()

# Collect a batch of observations
observations = []
for _ in range(15):
    action, _ = model.predict(obs, deterministic=True, action_masks=env.action_masks())
    print(action)
    obs, reward, terminated, truncated, _ = env.step(action)
    observations.append(obs)
    if terminated:
        obs, _ = env.reset()

observations = torch.tensor(observations, dtype=torch.float32, device="cpu")

obs_tensor = torch.tensor(obs).float().unsqueeze(0).requires_grad_(True)
action_dist = model.policy.get_distribution(obs_tensor)
loss = -action_dist.log_prob(torch.tensor([29]))
loss.backward()
saliency = obs_tensor.grad.data.abs().squeeze().numpy()

plt.bar(range(len(saliency)), saliency)
plt.show()
