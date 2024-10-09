import abc


class Opponent(abc.ABC):
    @abc.abstractmethod
    def initialize(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def make_action(self, observation, action_mask):
        raise NotImplementedError()
