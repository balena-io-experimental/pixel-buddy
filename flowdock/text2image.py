from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import emoji

import os
import textwrap
from string import ascii_letters

background = os.getenv("BACKGROUND_COLOUR") or "teal"
fontName = os.getenv("FONT") or "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
fontSize = os.getenv("FONT_SIZE") or 40
imagePath = "/data/my_data/"
DEBUG = (os.getenv("DEBUG") or "false") != "false"
class TextFunctions():

    def SaveTextToImage(my_text, filename=''):
        img = Image.new('RGBA', (720, 720), color=background)
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(fontName, fontSize)
        # font = ImageFont.load_default()

        # Calculate the average length of a single character of our font.
        # Note: this takes into account the specific font and font size.
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        # Translate this average length into a character count
        max_char_count = int( (img.size[0] * .75) / avg_char_width )
        # Create a wrapped text object using scaled character count
        text = textwrap.fill(text=my_text, width=max_char_count)

        try:
            w, h = draw.textsize(emoji.demojize(text))
        except UnicodeEncodeError:
            if DEBUG:
                print("Could not encode the message: " + my_text)
            return

        position = ( int((img.size[0] -w)/4), int((img.size[1] -h ) / 4))

        # Add text to the image
        pilmoji = Pilmoji(img)
        pilmoji.text(position, text, (255,255,255),font)
        # draw.text(xy=, text=text, font=font, fill='#ffffff', align='center')
        # img.show()
        img.save(imagePath + filename, 'png')


