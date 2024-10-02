from asap.engine.actions import ActionBuyFood


def validate_buy_food(action: ActionBuyFood, team_shop_state) -> bool:
    return not (
        action.shop_index not in team_shop_state.shop.food_shop.items or
        # food must not be already bought
        team_shop_state.shop.food_shop.already_bought(action.shop_index) or
        # must have enough money to buy the food
        team_shop_state.money < team_shop_state.shop.food_shop.price(action.shop_index) or
        # the target pet position must be occupied
        team_shop_state.team.pets[action.pet_position] is None
    )
