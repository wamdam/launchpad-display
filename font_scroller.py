from lib import launchpad
from lib import launchpad_layout
from PIL import Image, ImageFont, ImageDraw
import time

display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO, brightness=1.0, scale=False, debug=True)
#display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO_AMBIENT, brightness=2.0)

font = ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 11)

text_image = Image.new('RGB', (800, 8), color=0x000000)
draw = ImageDraw.Draw(text_image)
draw.text((0, -3), 'Kabeltrommel live. Insta: @kabeltrommel909. Like & Subscribe! Insert coin', font=font, fill=(255, 255, 255))

cropped_text_image = text_image.crop(text_image.getbbox())

display_image = Image.new('RGB', (8, 8), color=0x000000)
framerate = 10

while True:
    for offset in range(8, -(cropped_text_image.size[0] + 1), -1):
        t1 = time.time()
        display_image.paste(text_image, (offset, 0))
        display.setimage(display_image)
        t2 = time.time()
        sleeptime = 1/framerate - (t2 - t1)
        if sleeptime > 0:
            time.sleep(sleeptime)
