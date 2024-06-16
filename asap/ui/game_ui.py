# game_ui.py
import tkinter as tk
from PIL import Image, ImageTk
import importlib.resources as pkg_resources

import asap
from asap.ui.pet_icon import PetIcon
from asap.ui.food_icon import FoodIcon
from asap.ui.info_banner import InfoBanner
from asap.ui.actions import sell_pet, select_pet, deselect_pet, handle_team_click, swap_or_merge_pets, handle_item_click, deselect_item
from asap.ui.event_bindings import bind_freeze_pet, bind_freeze_food, roll, end_turn, freeze_pet, unfreeze_pet, freeze_food, unfreeze_food

class GameUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.team = game.teams[0]  # Assuming a single team for simplicity
        self.selected_pet_index = None
        self.selected_item = None
        self.selected_item_type = None  # 'food' or 'pet'
        self.title("Super Auto Pets")
        self.geometry("1500x1200")
        self.resizable(False, False)

        self.create_background()
        self.create_widgets()
        self.update_display()

    def create_background(self):
        with pkg_resources.path(asap.ui.img.backgrounds, 'Secret_Base.png') as bg_image_path:
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((1500, 1200), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

    def create_widgets(self):
        # Place the widgets on top of the background label
        self.info_banner = InfoBanner(self.bg_label)
        self.info_banner.pack(anchor='nw', pady=10, padx=20)  # Increase padx for spacing

        self.team_frame = tk.Frame(self.bg_label, bg='#8a9eb0')
        self.team_frame.pack(pady=20)
        self.team_frame.place(relx=0.1, rely=0.52, anchor='w')  # Moved up by 3%

        self.shop_frame = tk.Frame(self.bg_label, bg='#8a9eb0')
        self.shop_frame.pack(side=tk.LEFT, anchor='sw', padx=20, pady=20)
        self.shop_frame.place(relx=0.1, rely=0.78, anchor='w')  # Moved down by 3%

        self.food_shop_frame = tk.Frame(self.bg_label, bg='#8a9eb0')
        self.food_shop_frame.pack(side=tk.RIGHT, anchor='se', padx=20, pady=20)
        self.food_shop_frame.place(relx=0.9, rely=0.78, anchor='e')  # Moved down by 3%

        # Create frame for Sell and End Turn buttons
        self.button_frame = tk.Frame(self.bg_label, bg='#8a9eb0')
        self.button_frame.place(relx=0.95, rely=0.95, anchor='se')

        # Add Sell button
        self.sell_button = tk.Button(self.button_frame, text="Sell", font=('Helvetica', 27), command=lambda: sell_pet(self), width=7, height=1)
        self.sell_button.grid(row=0, column=0, padx=10)

        # Add End Turn button
        self.end_turn_button = tk.Button(self.button_frame, text="End Turn", font=('Helvetica', 27), command=lambda: end_turn(self.game, self.team, self.update_display), width=7, height=1)
        self.end_turn_button.grid(row=0, column=1, padx=10)

        # Initially hide the Sell button
        self.sell_button.grid_remove()

        # Add Roll button
        self.roll_button = tk.Button(self.bg_label, text="Roll", font=('Helvetica', 27), command=lambda: roll(self.game, self.team, self.update_display), width=7, height=1)
        self.roll_button.place(relx=0.05, rely=0.95, anchor='sw')

    def update_display(self):
        team_state = self.game.team_states[self.team]

        # Update info banner
        self.info_banner.update(money=team_state.money, health=self.team.health, turn=team_state.shop.turn)

        # Update team display
        for widget in self.team_frame.winfo_children():
            widget.destroy()
        for i in range(len(self.team.pets)):
            pet = self.team.pets[i]
            frame = tk.Frame(self.team_frame, width=112, height=112, bg='#8a9eb0', highlightbackground='yellow', highlightthickness=0)
            frame.pack_propagate(False)
            frame.pack(side=tk.LEFT, padx=5, pady=5)
            if pet:
                pet_icon = PetIcon(frame, pet, level=pet.level, on_click=lambda event, index=i: handle_team_click(self, index), in_team=True, width=112, height=112)
                pet_icon.pack()
            frame.bind("<Button-1>", lambda event, index=i: handle_team_click(self, index))  # Bind click to frame for empty slots
            if self.selected_pet_index is not None:
                if self.selected_pet_index == i:
                    frame.config(highlightbackground='blue', highlightthickness=2)
                elif self.selected_pet_index != i:
                    frame.config(highlightbackground='yellow', highlightthickness=2)
            elif self.selected_item is not None:
                frame.config(highlightbackground='green', highlightthickness=2)

        # Update pet shop display
        for widget in self.shop_frame.winfo_children():
            widget.destroy()
        for i, pet_item in enumerate(team_state.shop.pet_shop._items.values()):
            frame = tk.Frame(self.shop_frame, width=112, height=112, bg='#8a9eb0', highlightbackground='yellow', highlightthickness=0)
            frame.pack_propagate(False)
            frame.pack(side=tk.LEFT, padx=5, pady=5)
            if pet_item:
                pet_icon = PetIcon(frame, pet_item.item, price=pet_item.price, frozen=pet_item.is_frozen(), on_click=lambda event, index=i: handle_item_click(self, 'pet', index), width=112, height=112)
                bind_freeze_pet(pet_icon, lambda index=i: freeze_pet(self.game, self.team, self.update_display, index), lambda index=i: unfreeze_pet(self.game, self.team, self.update_display, index), i, pet_item.is_frozen())
                pet_icon.pack()
            if self.selected_item == i and self.selected_item_type == 'pet':
                frame.config(highlightbackground='blue', highlightthickness=2)

        # Update food shop display
        for widget in self.food_shop_frame.winfo_children():
            widget.destroy()
        for i, food_item in enumerate(team_state.shop.food_shop._items.values()):
            frame = tk.Frame(self.food_shop_frame, width=112, height=112, bg='#8a9eb0', highlightbackground='yellow', highlightthickness=0)
            frame.pack_propagate(False)
            frame.pack(side=tk.LEFT, padx=5, pady=5)
            if food_item:
                food_icon = FoodIcon(frame, food_item, frozen=food_item.is_frozen(), on_click=lambda event, index=i: handle_item_click(self, 'food', index), width=112, height=112)
                bind_freeze_food(food_icon, lambda index=i: freeze_food(self.game, self.team, self.update_display, index), lambda index=i: unfreeze_food(self.game, self.team, self.update_display, index), i, food_item.is_frozen())
                food_icon.pack()
            if self.selected_item == i and self.selected_item_type == 'food':
                frame.config(highlightbackground='blue', highlightthickness=2)

        # Bind deselect_item to any click on the background
        self.bg_label.bind("<Button-1>", lambda event: deselect_item(self))
