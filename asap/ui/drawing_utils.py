# drawing_utils.py
from PIL import Image, ImageDraw, ImageFont
import importlib.resources as pkg_resources
from asap.ui import img

def create_ellipse(draw, center, radius, text, font, color, text_color):
    x, y = center
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_x = x - (text_bbox[2] - text_bbox[0]) // 2
    text_y = y - (text_bbox[3] - text_bbox[1]) // 2
    draw.text((text_x, text_y), text, fill=text_color, font=font)


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
