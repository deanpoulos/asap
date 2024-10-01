from typing import Callable, Any


def updated_priorities(execute_phase: Callable[['Battle'], Any]):
    def wrapper(*args):
        self: 'Battle' = args[0]
        self.assign_pet_priorities()
        return execute_phase(self)

    return wrapper


def triggers_on_hurt_and_faint(execute_phase: Callable):
    def wrapper(*args):
        self: 'Battle' = args[0]
        output = execute_phase(self)
        self.phase_trigger_on_hurt_and_faint()

        return output

    return wrapper


