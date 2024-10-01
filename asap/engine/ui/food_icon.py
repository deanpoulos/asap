# food_icon.py
import tkinter as tk
from PIL import Image, ImageTk

from asap.engine.ui.drawing_utils import create_ellipse, fetch_image


class FoodIcon(tk.Label):
    def __init__(self, master, food, frozen=False, on_click=None, width=150, height=150, **kwargs):
        super().__init__(master, **kwargs)
        self.food = food
        self.price = food.price
        self.frozen = frozen
        self.width = width
        self.height = height

        # Fetch and resize food image
        food_image = fetch_image(type(food.item).__name__)
        food_image = food_image.resize((self.width, self.height), Image.Resampling.LANCZOS)

        # Draw additional info on the food image
        self.draw_additional_info(food_image)

        self.food_image = ImageTk.PhotoImage(food_image)
        self.configure(image=self.food_image, bg='#8a9eb0')

        if on_click:
            self.bind("<Button-1>", on_click)

    def draw_additional_info(self, image):
        create_ellipse(image, text=str(self.price), fill="yellow", outline="black", x=0.8 * self.width,
                       y=0.2 * self.height)
        if self.frozen:
            self.create_frozen_overlay(image)

    def create_frozen_overlay(self, image):
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 255, 128))
        image.paste(overlay, (0, 0), overlay)
