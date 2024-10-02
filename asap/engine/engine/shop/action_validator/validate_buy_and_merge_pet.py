from asap.engine.actions import ActionBuyAndMergePet


def validate_buy_and_merge_pet(action: ActionBuyAndMergePet, team_shop_state) -> bool:
    return not (
        action.shop_index not in team_shop_state.shop.pet_shop.items or
        team_shop_state.shop.pet_shop.already_bought(action.shop_index) or
        team_shop_state.money < team_shop_state.shop.pet_shop.price(action.shop_index) or
        team_shop_state.team.pets[action.pet_position] is None or
        action.pet_position not in team_shop_state.team.pets or
        team_shop_state.team.pets[action.pet_position] is None or
        not isinstance(team_shop_state.shop.pet_shop.items[action.shop_index].item, type(team_shop_state.team.pets[action.pet_position])) or
        team_shop_state.team.pets[action.pet_position].level == team_shop_state.game.settings.max_pet_level
    )
