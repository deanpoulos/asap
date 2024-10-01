from .action import Action
from .buy_food import ActionBuyFood
from .buy_and_place_pet import ActionBuyAndPlacePet
from .buy_and_merge_pet import ActionBuyAndMergePet
from .end_turn import ActionEndTurn
from .freeze_food import ActionFreezeFood
from .freeze_pet import ActionFreezePet
from .merge_pets import ActionMergePets
from .refresh_shop import ActionRefreshShop
from .sell_pet import ActionSellPet
from .swap_pets import ActionSwapPets
from .unfreeze_food import ActionUnfreezeFood
from .unfreeze_pet import ActionUnfreezePet

ALL_ACTIONS = [
    ActionBuyFood,
    ActionBuyAndPlacePet,
    ActionBuyAndMergePet,
    ActionEndTurn,
    ActionFreezeFood,
    ActionFreezePet,
    ActionMergePets,
    ActionRefreshShop,
    ActionSellPet,
    ActionSwapPets,
    ActionUnfreezeFood,
    ActionUnfreezePet,
]
