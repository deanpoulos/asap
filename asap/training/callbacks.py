from pathlib import Path
from typing import Dict, Any, Union

from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.callbacks import  BaseCallback
from torch.utils.tensorboard import SummaryWriter


class LogTeamAttackCallback(BaseCallback):
    """
    Sum's the primary team's attack and reports it to Tensorboard logs
    """

    def _on_step(self) -> bool:
        return True

    def __init__(self, verbose=0):
        super(LogTeamAttackCallback, self).__init__(verbose)

    def on_battle_end(self, env):
        team_attack = 0
        for pet in env.team_left.pets.values():
            if pet is not None:
                team_attack += pet.attack
        self.model.logger.record('custom/team_attack', team_attack)
        return True

class SaveModelRolloutEndCallback(BaseCallback):
    @staticmethod
    def model_name(index: Union[int, str]):
        return f"{index}_model.zip"

    def __init__(self, save_dir: Path, training_model: BaseAlgorithm = None, verbose=0):
        self.model = training_model
        self.index = 0
        self.save_directory = save_dir
        super(SaveModelRolloutEndCallback, self).__init__(verbose)

    def init_callback(self, model: "base_class.BaseAlgorithm") -> None:
        self.model = model
        self.save()

    def _on_step(self):
        return True

    def _on_rollout_end(self):
        self.save()

        return True

    def set_training_model(self, training_model: BaseAlgorithm):
        self.model = training_model

    def save(self):
        if self.model is None:
            raise AttributeError("Training model is not set. Did you call `set_training_model`?")
        self.model.save(self.save_directory / self.model_name(self.index))
        self.index += 1

    def save_as(self, save_name: str):
        if self.model is None:
            raise AttributeError("Training model is not set. Did you call `set_training_model`?")
        self.model.save(self.save_directory / save_name)

class HyperParameterDictionarySaverCallback(BaseCallback):
    def _on_step(self) -> bool:
        return True

    def __init__(self, hparams: dict):
        super().__init__()
        self.hparams = hparams

    def on_training_start(self, locals_: Dict[str, Any], globals_: Dict[str, Any]) -> None:
        writer = SummaryWriter(self.logger.dir)
        writer.add_hparams(hparam_dict=self.hparams, metric_dict={})
        writer.close()


class DeleteModelFromCacheCallback(BaseCallback):
    def __init__(self, model_cache: dict, model_name: str):
        super().__init__()
        self.model_name = model_name
        self.model_cache = model_cache

    def _on_step(self) -> bool:
        print("Deleting old best from cache...")
        del self.model_cache[self.model_name]
        return True
