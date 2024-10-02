from asap.engine.actions import ActionFreezeFood


def validate_freeze_food(action: ActionFreezeFood, team_shop_state) -> bool:
    return not (
        action.shop_index not in team_shop_state.shop.food_shop.items or
        # food must not be already bought
        team_shop_state.shop.food_shop.already_bought(action.shop_index) or
        # food must not already be frozen
        team_shop_state.shop.food_shop.items[action.shop_index].is_frozen()
    )
