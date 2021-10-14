import flowdock
import os
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from db_functions import DbFunctions

def WriteImageToFilesystem(filepath, fileContents):
    f = open("/data/my_data/" + filepath, "wb")
    f.write(fileContents)
    f.close()

background = os.getenv("BACKGROUND_COLOUR") or "white"
fontName = os.getenv("FONT") or "arial.ttf"
fontSize = os.getenv("FONT_SIZE") or 40

def txt2img(my_text):
    img = Image.new('L', (720, 720), color=background)
    draw = ImageDraw.Draw(img)
    # OS Error using line below, can't find font file...
    #font = ImageFont.truetype(fontName, fontSize)
    # Below works, but default font is terrible!
    font = ImageFont.load_default()
    # # print(message['content'])
    draw.text((0, 0), my_text, font=font)
    # # img.save(message['content']['file_name'])
    img.save('test5.png')

txt2img("Hello World!")

