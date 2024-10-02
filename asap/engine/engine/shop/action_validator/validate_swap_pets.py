from asap.engine.actions import ActionSwapPets
from asap.engine.team.states import TeamShopState


def validate_swap_pets(action: ActionSwapPets, team_shop_state: TeamShopState) -> bool:
    team = team_shop_state.team
    return not ((action.position_a not in team.pets or action.position_b not in team.pets) or
                (team.pets[action.position_a] is None and team.pets[action.position_b] is None))
