from lib import launchpad
from lib import launchpad_layout
from PIL import Image, ImageFont, ImageDraw
import time


#font = ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 7)
#font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 80, encoding="unic")
# get the line size

text = [[
    "##  ##",
    "## ## ",
    "###   ",
    "####  ",
    "## ## ",
    "##  ##",
], [
    "  ##  ",
    " #  # ",
    "##  ##",
    "######",
    "##  ##",
    "##  ##",
], [
    "##### ",
    "##  ##",
    "##### ",
    "##  ##",
    "##  ##",
    "##### ",
], [
    "######",
    "##    ",
    "####  ",
    "##    ",
    "##    ",
    "######",
], [
    "##    ",
    "##    ",
    "##    ",
    "##    ",
    "##    ",
    "######",
], [
    "######",
    "  ##  ",
    "  ##  ",
    "  ##  ",
    "  ##  ",
    "  ##  ",
], [
    "##### ",
    "##  ##",
    "##### ",
    "## ## ",
    "##  ##",
    "##  ##",
], [
    " #### ",
    "##  ##",
    "##  ##",
    "##  ##",
    "##  ##",
    " #### ",
], [
    "#    #",
    "##  ##",
    "######",
    "######",
    "##  ##",
    "##  ##",
], [
    "#    #",
    "##  ##",
    "######",
    "######",
    "##  ##",
    "##  ##",
], [
    "######",
    "##    ",
    "####  ",
    "##    ",
    "##    ",
    "######",
], [
    "##    ",
    "##    ",
    "##    ",
    "##    ",
    "##    ",
    "######",
]]

def draw_char(char):
    """ char is a list of text as above """
    width = len(char[0])
    height = len(char)
    image = Image.new('RGB', (width, height), color=0x000000)
    for x in range(width):
        for y in range(height):
            data = char[y][x]
            if data == '#':
                image.putpixel((x, y), (255, 255, 255))
    return image


#display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO, brightness=1.0)
display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO_AMBIENT, brightness=1.0, resize=False, debug=True)
width = display.pixelmap_max_x + 1
height = display.pixelmap_max_y + 1

framerate = 30

while True:
    for char in text:
        image = Image.new('RGB', (width, height), color=0x000000)
        image.paste(draw_char(char), (2, 2))
        draw = ImageDraw.Draw(image)
        for i in range(255, 50, -12):
            border_color = (i, i, 0)
            t1 = time.time()
            draw.line((0, 0, width, 0), fill=border_color, width=2)
            draw.line((0, 0, 0, height), fill=border_color, width=2)
            draw.line((0, height-2, width, height-2), fill=border_color, width=3)  # this has 3 lines!
            draw.line((width-2, 0, width-2, height), fill=border_color, width=2)
            display.setimage(image)
            sleep = 1/framerate - (time.time() - t1)
            if sleep > 0:
                time.sleep(sleep)
        time.sleep(.3)
