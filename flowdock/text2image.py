from PIL import Image, ImageDraw, ImageFont

import os
import textwrap
from string import ascii_letters


background = os.getenv("BACKGROUND_COLOUR") or "white"
fontName = os.getenv("FONT") or "arial.ttf"
fontSize = os.getenv("FONT_SIZE") or 40



def txt2img(my_text):
    img = Image.new('RGBA', (720, 720), color=background)
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()


    # Calculate the average length of a single character of our font.
    # Note: this takes into account the specific font and font size.
    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    # Translate this average length into a character count
    max_char_count = int( (img.size[0] * .75) / avg_char_width )
    # Create a wrapped text object using scaled character count
    text = textwrap.fill(text=my_text, width=max_char_count)

    w, h = draw.textsize(text)

    # Add text to the image
    draw.text(xy=((img.size[0] - w)/2, (img.size[1] - h) / 2), text=text, font=font, fill='#000000')

    return img

