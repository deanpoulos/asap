# actions.py
from asap.actions import ActionSellPet, ActionSwapPets, ActionMergePets, ActionBuyFood, ActionBuyAndPlacePet, ActionBuyAndMergePet

def sell_pet(game_ui):
    if game_ui.selected_pet_index is not None:
        game_ui.game.execute_action(ActionSellPet(game_ui.selected_pet_index), game_ui.team)
        game_ui.selected_pet_index = None
        game_ui.sell_button.grid_remove()  # Hide the Sell button when no pet is selected
        game_ui.update_display()

def select_pet(game_ui, pet_index):
    game_ui.selected_pet_index = pet_index
    game_ui.sell_button.grid()  # Show the Sell button when a pet is selected
    game_ui.update_display()

def deselect_pet(game_ui, event=None):
    game_ui.selected_pet_index = None
    game_ui.sell_button.grid_remove()  # Hide the Sell button when no pet is selected
    game_ui.update_display()

def handle_team_click(game_ui, pet_index):
    if game_ui.selected_item is not None:
        handle_item_use(game_ui, pet_index)
    elif game_ui.selected_pet_index is None:
        select_pet(game_ui, pet_index)
    elif game_ui.selected_pet_index == pet_index:
        deselect_pet(game_ui)
    else:
        swap_or_merge_pets(game_ui, pet_index)

def swap_or_merge_pets(game_ui, pet_index):
    pet_1 = game_ui.team.pets[game_ui.selected_pet_index]
    pet_2 = game_ui.team.pets[pet_index]
    if pet_2 is None:
        game_ui.game.execute_action(ActionSwapPets(game_ui.selected_pet_index, pet_index), game_ui.team)
    elif type(pet_1) == type(pet_2):
        game_ui.game.execute_action(ActionMergePets(game_ui.selected_pet_index, pet_index), game_ui.team)
    else:
        game_ui.game.execute_action(ActionSwapPets(game_ui.selected_pet_index, pet_index), game_ui.team)
    game_ui.selected_pet_index = None
    game_ui.sell_button.grid_remove()  # Hide the Sell button when no pet is selected
    game_ui.update_display()

def handle_item_click(game_ui, item_type, item_index):
    if game_ui.selected_item == item_index and game_ui.selected_item_type == item_type:
        deselect_item(game_ui)
    else:
        game_ui.selected_item = item_index
        game_ui.selected_item_type = item_type
        game_ui.selected_pet_index = None
        game_ui.sell_button.grid_remove()  # Hide the Sell button when an item is selected
        game_ui.update_display()

def handle_item_use(game_ui, pet_index):
    if game_ui.selected_item_type == 'food':
        game_ui.game.execute_action(ActionBuyFood(game_ui.selected_item, pet_index), game_ui.team)
    elif game_ui.selected_item_type == 'pet':
        if game_ui.team.pets[pet_index] is None:
            game_ui.game.execute_action(ActionBuyAndPlacePet(game_ui.selected_item, pet_index), game_ui.team)
        else:
            game_ui.game.execute_action(ActionBuyAndMergePet(game_ui.selected_item, pet_index), game_ui.team)
    game_ui.selected_item = None
    game_ui.selected_item_type = None
    game_ui.update_display()

def deselect_item(game_ui, event=None):
    if game_ui.selected_item is not None or game_ui.selected_item_type is not None:
        game_ui.selected_item = None
        game_ui.selected_item_type = None
        game_ui.update_display()
