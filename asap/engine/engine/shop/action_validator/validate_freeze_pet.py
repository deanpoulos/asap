from asap.engine.actions import ActionFreezePet


def validate_freeze_pet(action: ActionFreezePet, team_shop_state) -> bool:
    return not (
        # shop must contain item
        action.shop_index not in team_shop_state.shop.pet_shop.items or
        # pet must not be already bought
        team_shop_state.shop.pet_shop.already_bought(action.shop_index) or
        # pet must not already be frozen
        team_shop_state.shop.pet_shop.items[action.shop_index].is_frozen()
    )
