# drawing_utils.py
from PIL import Image, ImageDraw, ImageFont
import importlib.resources as pkg_resources
from asap.engine.ui import img


def create_ellipse(image, text, x, y, fill, outline="black", radius=15, margin=5):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Calculate bounding box for ellipse
    left = x - radius
    top = y - radius
    right = x + radius
    bottom = y + radius

    # Draw ellipse
    draw.ellipse([left, top, right, bottom], fill=fill, outline=outline)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = x - text_width / 2
    text_y = y - text_height / 2

    # Draw text
    draw.text((text_x, text_y), text, fill="black", font=font)

def create_rectangle(image, text, x, y, width, height, fill, outline="black"):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Calculate bounding box for rectangle
    left = x
    top = y
    right = x + width
    bottom = y + height

    # Draw rectangle
    draw.rectangle([left, top, right, bottom], fill=fill, outline=outline)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = x + (width - text_width) / 2
    text_y = y + (height - text_height) / 2

    # Draw text
    draw.text((text_x, text_y), text, fill="black", font=font)

def fetch_image(image_name):
    img_path = pkg_resources.path(img, f'{image_name}.png')
    with img_path as path:
        return Image.open(path).resize((100, 100))


def overlay_freeze_icon(image):
    """
    Overlays a 80% opacity light blue rectangle over an image to indicate it is frozen.
    """
    overlay = Image.new('RGBA', image.size, (173, 216, 230, int(255 * 0.8)))  # Light blue with 80% opacity
    combined = Image.alpha_composite(image.convert('RGBA'), overlay)
    return combined

def create_highlight_image(size):
    """
    Creates a transparent yellow highlight image of the given size.
    """
    highlight = Image.new('RGBA', size, (255, 255, 0, int(255 * 0.5)))  # Yellow with 50% opacity
    return highlight
