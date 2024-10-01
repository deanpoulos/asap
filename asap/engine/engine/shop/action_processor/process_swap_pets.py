from asap.engine.actions import ActionSwapPets
from asap.engine.engine.shop.action_processor._errors import *
from asap.engine.team.team import Team


def process_swap_pets(action: ActionSwapPets, team: Team, _):
    if (action.position_a not in team.pets or
        action.position_b not in team.pets) or (
            team.pets[action.position_a] is None and
            team.pets[action.position_b] is None):
        raise InvalidSwapError(action.position_a, action.position_b)

    pet_a = team.pets[action.position_a]
    team.pets[action.position_a] = team.pets[action.position_b]
    team.pets[action.position_b] = pet_a
