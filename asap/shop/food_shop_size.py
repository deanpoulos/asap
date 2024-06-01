from asap.shop.constants import TIER_1_SHOP_SIZE, TIER_2_SHOP_SIZE, TIER_3_SHOP_SIZE, TIER_4_SHOP_SIZE, \
    TIER_5_SHOP_SIZE, TIER_6_SHOP_SIZE


def pet_shop_size(turn: int) -> int:
    if turn < 3:
        return TIER_1_SHOP_SIZE
    elif turn < 5:
        return TIER_2_SHOP_SIZE
    elif turn < 7:
        return TIER_3_SHOP_SIZE
    elif turn < 9:
        return TIER_4_SHOP_SIZE
    elif turn < 11:
        return TIER_5_SHOP_SIZE
    else:
        return TIER_6_SHOP_SIZE
