import random
from pathlib import Path

from stable_baselines3.common.callbacks import BaseCallback

def model_name(index: int):
    return f"{index}.model"

class Callback(BaseCallback):
    def __init__(self, model, save_directory: Path, verbose=0):
        self.index = 0
        self.model = model
        self.save_directory = save_directory
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
    def __init__(self, model, save_directory: Path, probability_to_load_random_model: float):
        self.model = model
        self.save_directory = save_directory
        self.probability_to_load_random_model = probability_to_load_random_model

        self.adversaries = {}
        self.callback = Callback(self.model, save_directory)

    def make_adversary(self, model_index: int = None):
        if model_index is None:
            if self.callback.index <= 1:
                model_index = 0
            else:
                if random.uniform(0, 1) < self.probability_to_load_random_model:
                    model_index = random.randint(0, self.callback.index - 1)
                else:
                    model_index = self.callback.index - 1

        if model_index not in self.adversaries:
            model_to_load = self.save_directory / model_name(model_index)
            self.adversaries[model_index] = type(self.model).load(model_to_load)

        return self.adversaries[model_index]
