from asap.engine.actions import ActionUnfreezePet


def validate_unfreeze_pet(action: ActionUnfreezePet, team_shop_state) -> bool:
    return not (
        action.shop_index not in team_shop_state.shop.pet_shop.items or
        team_shop_state.shop.pet_shop.already_bought(action.shop_index) or
        not team_shop_state.shop.pet_shop.items[action.shop_index].is_frozen()
    )
