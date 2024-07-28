from lib import launchpad
from lib import launchpad_layout
from PIL import Image
import time

display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO, brightness=1.8, scale=False, debug=True)
image = Image.open('test/potions.png')

def get_sprite(index, image):
    y = (index * 8) // 32 * 8
    x = (index * 8) % 32
    sprite = Image.new('RGB', (8, 8), color=0x000000)
    sprite.paste(image, (-x, -y))
    return sprite

while True:
    # walk towards us
    for i in range(12):
        sprite = get_sprite(i, image)
        display.setimage(sprite)
        time.sleep(.2)
