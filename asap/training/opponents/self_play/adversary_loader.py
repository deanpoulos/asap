import abc
import random
from pathlib import Path
from typing import Type

from stable_baselines3.common.base_class import BaseAlgorithm

from asap.training.callbacks import SaveModelRolloutEndCallback


class OpponentLoader(abc.ABC):
    def __init__(self, model_type: Type[BaseAlgorithm]):
        self.model_type = model_type

    @abc.abstractmethod
    def load(self) -> BaseAlgorithm:
        raise NotImplementedError()

class OpponentSaverLoaderBestOrRandom(OpponentLoader):
    def __init__(self, model_type: Type[BaseAlgorithm],
                 saver_callback: SaveModelRolloutEndCallback,
                 probability_to_load_random_model: float,
                 path_to_initial_best_model: Path | str | None = None):

        super().__init__(model_type)
        self.saver = saver_callback
        self.probability_to_load_random_model = probability_to_load_random_model
        self.path_to_initial_best_model = path_to_initial_best_model
        self.opponents = {}

        if self.path_to_initial_best_model is not None:
            self.opponents['best'] = load_model(model_type, path_to_initial_best_model)


    def load(self) -> BaseAlgorithm:
        if self.saver.index <= 1:
            model_index = 0
        else:
            if random.uniform(0, 1) < self.probability_to_load_random_model:
                model_index = random.randint(0, self.saver.index - 1)
            else:
                model_index = 'best'

        if model_index not in self.opponents:
            self.opponents[model_index] = load_model(
                self.model_type, self.saver.save_directory / f"{model_index}_model"
            )

        return self.opponents[model_index]


class OpponentLoaderBest(OpponentLoader):
    def __init__(self, model_type: Type[BaseAlgorithm], load_dir: Path):
        super().__init__(model_type)
        self.load_dir = load_dir

    def load(self) -> BaseAlgorithm:
        return load_model(self.model_type, self.load_dir / 'best_model')


def load_model(model_type: Type[BaseAlgorithm], model_path: Path) -> BaseAlgorithm:
    return model_type.load(model_path)
