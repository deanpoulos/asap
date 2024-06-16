def validate_refresh_shop(team_shop_state):
    shop = team_shop_state.shop

    roll_price = shop.roll_price
    return team_shop_state.money >= roll_price
