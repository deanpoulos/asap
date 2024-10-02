from asap.engine.actions import ActionSellPet


def validate_sell_pet(action: ActionSellPet, team_shop_state) -> bool:
    return team_shop_state.team.pets[action.pet_position] is not None
