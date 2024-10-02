from asap.engine.actions import ActionBuyAndPlacePet


def validate_buy_and_place_pet(action: ActionBuyAndPlacePet, team_shop_state) -> bool:
    return not (
        action.shop_index not in team_shop_state.shop.pet_shop.items or
        team_shop_state.shop.pet_shop.already_bought(action.shop_index) or
        team_shop_state.money < team_shop_state.shop.pet_shop.price(action.shop_index) or
        team_shop_state.team.is_full() or
        team_shop_state.team.pets[action.pet_position] is not None
    )