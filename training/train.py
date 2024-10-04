import os
from datetime import datetime
from pathlib import Path

from stable_baselines3.common.callbacks import EvalCallback

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

from asap.training.environment.environment import AsapEnvironmentTwoPlayer
from asap.training.scenarios.mosquito_upgrade_to_superduck_scenario import mosquito_to_superduck_game_settings

from asap.training.adversary import AdversaryLoader
from asap.training.callbacks import CustomTensorboardCallback

log_dir = 'logs'
load_dir = save_dir = Path('runs') / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
tmp_dir = Path('/tmp')
os.makedirs(save_dir, exist_ok=True)

def make_env():
    env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings)
    env = ActionMasker(env, env.mask_fn)
    return env

env = make_env()

model = MaskablePPO(
    MaskableActorCriticPolicy,
    env,
    n_steps=10,
    batch_size=4,
    ent_coef=0.,
    verbose=0,
    device='cuda',
    learning_rate=3e-4,
    tensorboard_log=log_dir
)

adversary_loader = AdversaryLoader(model, load_dir, save_dir, probability_to_load_random_model=0.2)
env.set_adversary_loader(adversary_loader)
env.adversary_loader.callback.save()

eval_env = make_env()
eval_adversary_loader = AdversaryLoader(model, load_dir, tmp_dir, probability_to_load_random_model=1)
eval_env.set_adversary_loader(eval_adversary_loader)
eval_env.adversary_loader.callback.save()
eval_env.reset()

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=save_dir,
    log_path=log_dir,
    n_eval_episodes=20,
    eval_freq=40,
    deterministic=True,
    render=False
)

team_power_callback = CustomTensorboardCallback(env, model, verbose=1)

model.learn(
    total_timesteps=1e6,
    callback=[env.adversary_loader.callback, team_power_callback, eval_callback]
)
