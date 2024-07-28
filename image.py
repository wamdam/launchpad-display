from lib import launchpad
from lib import launchpad_layout
from PIL import Image
import time

display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO, brightness=2.0)
#display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO_AMBIENT, brightness=2.0)
#image = Image.open('t1.gif')
image = Image.open('test/giphy.webp')

# To iterate through the entire gif
while True:
    image.seek(0)
    try:
        while 1:
            t1 = time.time()
            image.seek(image.tell()+1)
            display.setimage(image)
            t2 = time.time()
            diff = t2-t1
            required_duration = image.info['duration'] / 1000
            required_sleep = required_duration - diff
            print(diff, required_duration, required_sleep)
            if required_sleep > 0:
                time.sleep(required_sleep)
            # do something to im
    except EOFError:
        pass # end of sequence
