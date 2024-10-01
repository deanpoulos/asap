# pet_icon.py
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

from asap.engine.ui.drawing_utils import create_ellipse, create_rectangle, fetch_image


class PetIcon(tk.Label):
    def __init__(self, master, pet, level=1, price=None, frozen=False, on_click=None, in_team=False, width=150,
                 height=150, **kwargs):
        super().__init__(master, **kwargs)
        self.pet = pet
        self.level = level
        self.price = price
        self.frozen = frozen
        self.in_team = in_team
        self.width = width
        self.height = height

        # Fetch and resize pet image
        pet_image = fetch_image(type(pet).__name__)
        pet_image = pet_image.resize((self.width, self.height), Image.Resampling.LANCZOS)

        # Draw additional info on the pet image
        self.draw_additional_info(pet_image)

        self.pet_image = ImageTk.PhotoImage(pet_image)
        self.configure(image=self.pet_image, bg='#8a9eb0')

        if on_click:
            self.bind("<Button-1>", on_click)

    def draw_additional_info(self, image):
        if self.price is not None:
            create_ellipse(image, text=str(self.price), fill="yellow", outline="black", x=0.8 * self.width,
                           y=0.2 * self.height)
        create_ellipse(image, text=str(self.pet.attack), fill="gray", outline="black", x=0.2 * self.width,
                       y=0.8 * self.height)
        create_ellipse(image, text=str(self.pet.health), fill="red", outline="black", x=0.8 * self.width,
                       y=0.8 * self.height)
        if self.in_team:
            self.draw_level(image)
            self.draw_exp_bar(image)
        if self.frozen:
            self.create_frozen_overlay(image)

    def draw_level(self, image):
        level_text = f"LVL{self.level}"
        create_rectangle(image, text=level_text, x=5, y=5, width=50, height=20, fill="blue", outline="black")

    def draw_exp_bar(self, image):
        draw = ImageDraw.Draw(image)
        exp_boxes = 2 if self.level == 1 else 3
        exp_fill = self.pet.exp - (2 if self.level == 2 else 0)
        box_width = (self.width // 2) // exp_boxes  # Only take half the width
        box_height = 10
        for i in range(exp_boxes):
            left = self.width - (exp_boxes - i) * box_width - 5
            right = left + box_width - 5
            top = 5
            bottom = top + box_height
            color = "darkgray" if i >= exp_fill else "lightblue"
            draw.rectangle([left, top, right, bottom], fill=color, outline="black")

    def create_frozen_overlay(self, image):
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 255, 128))
        image.paste(overlay, (0, 0), overlay)
