import os.path
import random
from pathlib import Path

from stable_baselines3.common.callbacks import BaseCallback

def model_name(index: int):
    return f"{index}_model.zip"

class Callback(BaseCallback):
    def __init__(self, model, save_dir: Path, verbose=0):
        self.index = 0
        self.model = model
        self.save_directory = save_dir
        super(Callback, self).__init__(verbose)

    def _on_step(self):
        return True

    def _on_rollout_end(self):
        self.save()
        self.index += 1

        return True

    def save(self):
        self.model.save(self.save_directory / model_name(self.index))

class AdversaryLoader:
    def __init__(self, model, load_dir: Path, save_dir: Path, probability_to_load_random_model: float):
        self.model = model
        self.load_dir = load_dir
        self.save_dir = save_dir
        self.probability_to_load_random_model = probability_to_load_random_model

        self.adversaries = {}
        self.callback = Callback(self.model, save_dir)

    def make_adversary(self, model_index: int = None):
        if model_index is None:
            if self.callback.index <= 1:
                model_index = 0
            else:
                if random.uniform(0, 1) < self.probability_to_load_random_model:
                    model_index = random.randint(0, self.callback.index - 1)
                else:
                    if os.path.exists(self.load_dir / 'best_model.zip'):
                        model_index = 'best'
                    else:
                        model_index = self.callback.index - 1

        if model_index not in self.adversaries:
            model_to_load = self.load_dir / model_name(model_index)
            self.adversaries[model_index] = type(self.model).load(model_to_load)

        return self.adversaries[model_index]

class AdversaryEndTurn(AdversaryLoader):
    def make_adversary(self, model_index: int = None):
        class Model:
            def predict(self, *args):
                return 0

        return Model()