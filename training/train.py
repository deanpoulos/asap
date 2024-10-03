import os
from datetime import datetime
from pathlib import Path

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

from asap.engine.engine.game_settings import GameSettings
from asap.environment.environment import AsapEnvironmentTwoPlayer

game_settings = GameSettings(num_teams=2)

# save_directory = Path('runs') / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
save_directory = Path('runs')
os.makedirs(save_directory, exist_ok=True)

def make_adversary_callback():
    return MaskablePPO.load(save_directory / '0.model')

env = AsapEnvironmentTwoPlayer(game_settings, make_adversary_callback)  # Initialize env
env = ActionMasker(env, env.mask_fn)  # Wrap to enable masking

model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1, device='cuda')
model.save(save_directory / f'0.model')

def callback(*args):
    timestep = args[0]["self"].num_timesteps
    # print(timestep)
    # model.save(save_directory / f'0.model')

    return True

model.learn(
    total_timesteps=100_000,
    callback=callback,
    progress_bar=True
)
