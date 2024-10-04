import os
from datetime import datetime
from pathlib import Path

from stable_baselines3.common.vec_env import SubprocVecEnv

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

from asap.engine.engine.game_settings import GameSettings
from asap.engine.pets import Duck, Mosquito, Pet
from asap.engine.shop.settings import SettingsPetShop, SettingsFoodShop
from asap.training.environment.environment import AsapEnvironmentTwoPlayer

from asap.training.adversary import AdversaryLoader

class SuperDuck(Duck):
    base_attack = 10
    base_health = 10

    def __init__(self):
        super().__init__(attack=self.base_attack, health=self.base_health)

game_settings = GameSettings(
    num_teams=2,
    starting_team_health=1,
    max_turn=1,
    settings_pet_shop=SettingsPetShop(
        TIER_1_PETS=[SuperDuck, Mosquito],
        TIER_2_PETS=[Mosquito],
        TIER_3_PETS=[Mosquito],
        MAX_ITEMS=5
    ),
    settings_food_shop=SettingsFoodShop(
        MAX_ITEMS=3
    ),
    max_team_size=2
)

save_directory = Path('runs') / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(save_directory, exist_ok=True)

def make_env():
    env = AsapEnvironmentTwoPlayer(game_settings)  # Initialize env
    env = ActionMasker(env, env.mask_fn)  # Wrap to enable masking
    return env

env = make_env()

model = MaskablePPO(
    MaskableActorCriticPolicy,
    env,
    n_steps=2048,
    verbose=1,
    device='cuda',
    learning_rate=1e-4,
    tensorboard_log='logs'
)

adversary_loader = AdversaryLoader(model, save_directory, probability_to_load_random_model=0.5)
env.set_adversary_loader(adversary_loader)

env.adversary_loader.callback.save()

model.learn(
    total_timesteps=1e6,
    callback=env.adversary_loader.callback,
    progress_bar=True
)
