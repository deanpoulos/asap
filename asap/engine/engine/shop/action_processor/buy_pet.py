from asap.engine.actions import ActionBuyAndPlacePet, ActionBuyAndMergePet
from asap.engine.pets import Pet
from asap.engine.shop.pet_shop import PetShop
from asap.engine.team.states import TeamShopState


def buy_pet(team_shop_state: TeamShopState,
            shop: PetShop,
            action: ActionBuyAndPlacePet | ActionBuyAndMergePet) -> Pet:

    item_price = shop.price(action.shop_index)
    team_shop_state.money -= item_price
    pet = team_shop_state.shop.buy_pet(action.shop_index)

    return pet
