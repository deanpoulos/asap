# pet_icon.py
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from asap.ui.drawing_utils import fetch_image, overlay_freeze_icon, create_ellipse


def create_pet_icon(pet, price=None, level=None, frozen=False):
    pet_name = type(pet).__name__
    pet_image = fetch_image(pet_name)

    # Calculate padding
    margin = 5
    max_diameter = 30  # Reduced size of circles by 25%
    radius = max_diameter // 2 + margin

    # Create a new image with padding
    new_size = (pet_image.width + radius * 2, pet_image.height + radius * 2 + 20)  # Extra space for exp bar
    new_image = Image.new("RGBA", new_size, (255, 255, 255, 0))
    new_image.paste(pet_image, (radius, radius))

    if frozen:
        new_image = overlay_freeze_icon(new_image)

    draw = ImageDraw.Draw(new_image)
    font = ImageFont.truetype("arial", 18)  # Adjust font size

    # Draw attack in grey bubble
    attack_center = (radius, new_size[1] - (radius + margin) - 20)  # Adjust for exp bar
    create_ellipse(draw, attack_center, radius, str(pet.attack), font, "grey", "white")

    # Draw health in red bubble
    health_center = (new_size[0] - (radius + margin), new_size[1] - (radius + margin) - 20)  # Adjust for exp bar
    create_ellipse(draw, health_center, radius, str(pet.health), font, "red", "white")

    if price is not None:
        # Draw price in yellow bubble
        price_center = (new_size[0] - (radius + margin), radius)
        create_ellipse(draw, price_center, radius, str(price), font, "yellow", "black")
    elif level is not None:
        # Draw level in blue rectangle
        level_text = f"LVL{level}"
        level_bbox = draw.textbbox((0, 0), level_text, font=font)
        level_width = level_bbox[2] - level_bbox[0] + 2 * margin
        level_height = level_bbox[3] - level_bbox[1] + 2 * margin
        draw.rectangle([(margin, margin), (margin + level_width, margin + level_height)], fill="blue")
        draw.text((margin + (level_width - (level_bbox[2] - level_bbox[0])) // 2,
                   margin + (level_height - (level_bbox[3] - level_bbox[1])) // 2), level_text, fill="white", font=font)

        # Draw exp bar in top-right corner, right-aligned
        exp_bar_width = 15  # 50% wider
        exp_bar_height = 7.5  # 50% shorter
        exp_bar_spacing = 5

        num_boxes = 2 if level == 1 else 3
        filled_boxes = pet.exp if level == 1 else pet.exp - 2

        exp_bar_x_start = new_size[0] - margin - (num_boxes * (exp_bar_width + exp_bar_spacing) - exp_bar_spacing)
        exp_bar_y_start = margin

        for i in range(num_boxes):
            x0 = exp_bar_x_start + i * (exp_bar_width + exp_bar_spacing)
            y0 = exp_bar_y_start
            x1 = x0 + exp_bar_width
            y1 = y0 + exp_bar_height

            if i < filled_boxes:
                draw.rectangle([(x0, y0), (x1, y1)], fill="green")
            else:
                draw.rectangle([(x0, y0), (x1, y1)], fill="darkgrey", outline="black")

    return ImageTk.PhotoImage(new_image)


class PetIcon(tk.Canvas):
    def __init__(self, master, pet, price=None, level=None, frozen=False, on_click=None, **kwargs):
        super().__init__(master, bg="black", highlightthickness=0, **kwargs)
        self.pet_image = create_pet_icon(pet, price=price, level=level, frozen=frozen)
        self.create_image(0, 0, image=self.pet_image, anchor="nw")
        self.pet = pet
        self.price = price
        self.level = level
        self.frozen = frozen

        if on_click:
            self.bind("<Button-1>", on_click)
