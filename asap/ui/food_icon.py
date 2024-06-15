# food_icon.py
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from drawing_utils import fetch_image, overlay_freeze_icon, create_ellipse

def create_food_icon(food, frozen=False, price=None):
    food_name = type(food.item).__name__
    food_image = fetch_image(food_name)

    # Calculate padding
    margin = 5
    max_diameter = 30  # Reduced size of circles by 25%
    radius = max_diameter // 2 + margin

    # Create a new image with padding
    new_size = (food_image.width + radius * 2, food_image.height + radius * 2)
    new_image = Image.new("RGBA", new_size, (255, 255, 255, 0))
    new_image.paste(food_image, (radius, radius))

    if frozen:
        new_image = overlay_freeze_icon(new_image)

    draw = ImageDraw.Draw(new_image)
    font = ImageFont.truetype("arial", 18)  # Adjust font size

    # Draw price in yellow bubble
    price = food.price
    price_center = (new_size[0] - (radius + margin), radius)
    create_ellipse(draw, price_center, radius, str(price), font, "yellow", "black")

    return ImageTk.PhotoImage(new_image)

class FoodIcon(tk.Label):
    def __init__(self, master, food, frozen=False, price=None, on_click=None, **kwargs):
        self.food_image = create_food_icon(food, frozen=frozen, price=price)
        super().__init__(master, image=self.food_image, **kwargs)
        self.food = food
        self.frozen = frozen
        self.price = price

        if on_click:
            self.bind("<Button-1>", on_click)
