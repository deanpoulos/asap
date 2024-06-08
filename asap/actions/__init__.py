from .action import Action
from .buy_food import ActionBuyFood
from .buy_pet import ActionBuyPet
from .end_turn import ActionEndTurn
from .freeze_food import ActionFreezeFood
from .freeze_pet import ActionFreezePet
from .merge_pets import ActionMergePet
from .refresh_shop import ActionRefreshShop
from .sell_pet import ActionSellPet
from .swap_pets import ActionSwapPets

ALL_ACTIONS = [
    ActionBuyFood,
    ActionBuyPet,
    ActionEndTurn,
    ActionFreezeFood,
    ActionFreezePet,
    ActionMergePet,
    ActionRefreshShop,
    ActionSellPet,
    ActionSwapPets
]
