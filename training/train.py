import os
from datetime import datetime
from pathlib import Path

from sb3_contrib.common.maskable.policies import MaskableMultiInputActorCriticPolicy, MaskableActorCriticPolicy
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

from asap.training.environment.environment import AsapEnvironmentTwoPlayer
from asap.training.opponents.self_play.adversary_loader import OpponentSaverLoaderBestOrRandom, OpponentLoaderBest
from asap.training.opponents.self_play.adversary_self_play import OpponentSelfPlay
from asap.training.scenarios.mosquito_upgrade_to_superduck_scenario.settings import mosquito_to_superduck_game_settings

from asap.training.callbacks import LogTeamAttackCallback, HyperParameterDictionarySaverCallback, \
    SaveModelRolloutEndCallback, DeleteModelFromCacheCallback

# Define IO directories
date_time_path = datetime.now().strftime("%Y-%m-%d"),  datetime.now().strftime("%H-%M-%S")
tensorboard_log_dir = Path('logs') / date_time_path[0] / date_time_path[1]
save_dir = Path('runs') / date_time_path[0] / date_time_path[1]
os.makedirs(save_dir, exist_ok=True)

# Set hyperparameters
training_opponent_hparams = {
    "probability_to_load_random_model":  0.2,
    # "path_to_initial_best_model": "/media/dean/Dean's PC Extension Drive/Training Data/Asap/runs/2024-10-07/21-32-14/best_model.zip"
}
eval_hparams = {
    "n_eval_episodes": 20,
    "eval_freq": 1000,
}
eval_opponent_hparams = {
    "probability_to_load_random_model": 0.0,
}
env_hparams = {
    "use_flat_observations": True,
    "observe_opponent_after_battle": False
}
model_hparams = {
    "n_steps": 2048,
    "batch_size": 64,
    "gae_lambda": 0.95,
    "ent_coef": 0.1,
    "gamma": 0.99,
    "learning_rate": 1e-4,
}
training_hparams = {
    "total_timesteps": int(1e6)
}

# Make the environment
saver_callback = SaveModelRolloutEndCallback(save_dir)
team_attack_callback = LogTeamAttackCallback()
opponent_loader = OpponentSaverLoaderBestOrRandom(MaskablePPO, saver_callback, **training_opponent_hparams)
opponent = OpponentSelfPlay(loader=opponent_loader)

env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings, opponent, **env_hparams, verbose=0)
env = ActionMasker(env, env.mask_fn)


# Make the model
args = {
    **model_hparams,
    "verbose": 0,
    "device": 'cuda',
    "tensorboard_log": tensorboard_log_dir
}

if env_hparams["use_flat_observations"]:
    policy_type = MaskableActorCriticPolicy
else:
    policy_type = MaskableMultiInputActorCriticPolicy

model = MaskablePPO(policy_type, env, **args)
saver_callback.init_callback(model)
if not opponent_loader.path_to_initial_best_model:
    saver_callback.save_as('best_model.zip')  # randomly seed initial best model

# Add evaluation to the training process
eval_opponent_loader = OpponentLoaderBest(MaskablePPO, save_dir)
eval_opponent = OpponentSelfPlay(loader=eval_opponent_loader)
# eval_adversary = OptimalMosquitoUpgradeToSuperduckScenarioOpponent(
#     make_possible_actions_inverse_mapping(mosquito_to_superduck_game_settings)
# )
eval_env = AsapEnvironmentTwoPlayer(mosquito_to_superduck_game_settings, eval_opponent, team_attack_callback.on_battle_end, **env_hparams, verbose=1)
eval_env = ActionMasker(eval_env, eval_env.mask_fn)

# Add other callbacks
callbacks = [
    saver_callback,
    team_attack_callback,
    MaskableEvalCallback(
        eval_env,
        best_model_save_path=save_dir,
        log_path=tensorboard_log_dir,
        callback_on_new_best=DeleteModelFromCacheCallback(opponent_loader.opponents, 'best'),
        **eval_hparams,
        deterministic=True,
        render=False
    ),
    HyperParameterDictionarySaverCallback({**model_hparams, **training_hparams, **training_opponent_hparams, **eval_hparams, **env_hparams}),
]

# Learn!
model.learn(**training_hparams, callback=callbacks)
