from asap.engine.actions import ActionUnfreezeFood


def validate_unfreeze_food(action: ActionUnfreezeFood, team_shop_state) -> bool:
    return not (
        action.shop_index not in team_shop_state.shop.food_shop.items or
        team_shop_state.shop.food_shop.already_bought(action.shop_index) or
        not team_shop_state.shop.food_shop.items[action.shop_index].is_frozen()
    )
