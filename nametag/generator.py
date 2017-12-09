import PIL
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

cwd = os.path.dirname(os.path.realpath(__file__))
fonts_dir = cwd
img_dir = cwd

#FONT_NUMBERS:
#    0: normal
#    1: light
#    2: bold
FONTS = ["/OpenSans-Regular.ttf", "/OpenSans-Light.ttf", "/OpenSans-Bold.ttf"]

#list of ((x,y), text, (r,g,b), font_number, font_size)
directions = [
              ((0,0), "abcdefghijklmnopQRSTUVWXYZ", (0,0,0), 0, 25),
              ((0,200), "hello this is a test", (0,0,0), 2, 20)
             ]

def create_nametag(w, h, filename="test.png"):
    '''
    creates a nametag of dimensions wxh to save as filename
    follows the directions specified in directions
    '''
    img = Image.new("RGBA", (w,h), (255,255,255))
    for direction in directions:
        add_text(img, direction)
    img.save(img_dir+"/"+filename)

def add_text(img, direction):
    '''
    adds one direction to img as specified in the format
    (x,y), text, (r,g,b), font_number, font_size
    '''
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fonts_dir+FONTS[direction[3]], direction[4])
    draw.text(direction[0], direction[1], direction[2], font=font)

create_nametag(800,600)