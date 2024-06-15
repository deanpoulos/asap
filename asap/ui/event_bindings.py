# event_bindings.py
from asap.actions import ActionFreezePet, ActionUnfreezePet, ActionFreezeFood, ActionUnfreezeFood, ActionRefreshShop, ActionEndTurn

def bind_freeze_pet(widget, freeze_action, unfreeze_action, index, is_frozen):
    if is_frozen:
        widget.bind("<Button-3>", lambda event: unfreeze_action(index))
    else:
        widget.bind("<Button-3>", lambda event: freeze_action(index))

def bind_freeze_food(widget, freeze_action, unfreeze_action, index, is_frozen):
    if is_frozen:
        widget.bind("<Button-3>", lambda event: unfreeze_action(index))
    else:
        widget.bind("<Button-3>", lambda event: freeze_action(index))

def roll(game, team, update_display):
    game.execute_action(ActionRefreshShop(), team)
    update_display()

def end_turn(game, team, update_display):
    game.execute_action(ActionEndTurn(), team)
    update_display()

def freeze_pet(game, team, update_display, shop_index):
    game.execute_action(ActionFreezePet(shop_index), team)
    update_display()

def unfreeze_pet(game, team, update_display, shop_index):
    game.execute_action(ActionUnfreezePet(shop_index), team)
    update_display()

def freeze_food(game, team, update_display, shop_index):
    game.execute_action(ActionFreezeFood(shop_index), team)
    update_display()

def unfreeze_food(game, team, update_display, shop_index):
    game.execute_action(ActionUnfreezeFood(shop_index), team)
    update_display()
