from lib import launchpad
from lib import launchpad_layout
from PIL import Image
import time

display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO, brightness=1.6, scale=False, debug=True)
image = Image.open('test/mervin_black.png')

def get_sprite(index, image):
    y = (index * 8) // 32 * 8
    x = (index * 8) % 32
    sprite = Image.new('RGB', (8, 8), color=0x000000)
    sprite.paste(image, (-x, -y))
    return sprite

while True:
    # walk towards us
    #for i in range(16):
    #    sprite = get_sprite(8, image)
    #    display.setimage(sprite)
    #    time.sleep(.2)
    #    sprite = get_sprite(9, image)
    #    display.setimage(sprite)
    #    time.sleep(.2)
    #    sprite = get_sprite(10, image)
    #    display.setimage(sprite)
    #    time.sleep(.2)
    #    sprite = get_sprite(11, image)
    #    display.setimage(sprite)
    #    time.sleep(.2)
    for i in range(16):
        sprite = get_sprite(12, image)
        display.setimage(sprite)
        time.sleep(.2)
        sprite = get_sprite(13, image)
        display.setimage(sprite)
        time.sleep(.2)
        sprite = get_sprite(14, image)
        display.setimage(sprite)
        time.sleep(.2)
        sprite = get_sprite(15, image)
        display.setimage(sprite)
        time.sleep(.2)
