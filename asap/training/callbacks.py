from stable_baselines3.common.callbacks import  BaseCallback


class CustomTensorboardCallback(BaseCallback):
    def __init__(self, env, model, verbose=0):
        super(CustomTensorboardCallback, self).__init__(verbose)
        self.env = env
        self.model = model

    def _on_step(self) -> bool:
        if self.training_env.envs[0].game.is_over():
        # if self.locals['dones'][0]:
            # Log `env.game.team_left.base_attack` to TensorBoard
            try:
                team_attack = 0
                for pet in self.env.team_left.pets.values():
                    if pet is not None:
                        team_attack += pet.attack
                self.model.logger.record('custom/team_attack', team_attack)
            except AttributeError as e:
                if self.verbose > 0:
                    print(f"AttributeError during logging: {e}")
        return True

    def _on_training_end(self):
        # Close the TensorBoard writer when training ends
        if self.writer:
            self.writer.close()