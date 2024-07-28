import mido
import time
import colors
import launchpad_layout
import PIL

LP_DEVICE_NAME = 'Launchpad Pro MK3:Launchpad Pro MK3 LPProMK3 MIDI 32:0'
LP_SYSEX_HEADER = [0x00, 0x20, 0x29, 0x02, 0x0E]

class Display():
    p_out = None
    p_in = None

    def __init__(self, pixelmap, brightness=1.0):
        """ pixelmap is a dict of tuples: note-value (e.g. launchpad_layout.LAUNCHPAD_MK3_PRO) 
        """
        self.p_out = mido.open_output(LP_DEVICE_NAME)
        self.p_in = mido.open_input(LP_DEVICE_NAME)
        self.pixelmap = pixelmap
        self.pixelmap_max_x = max([d[0] for d in self.pixelmap.keys()])
        self.pixelmap_max_y = max([d[1] for d in self.pixelmap.keys()])
        self.brightness = brightness

        app_version = self.check_launchpad()
        if not app_version:
            raise ValueError("This is no launchpad")
        #print("Found Launchpad. App-Version: {}".format(app_version))
        if not self.set_programmer_mode():
            raise ValueError("Setting programmer mode didn't work")
        #print("Set programmer mode")

    def check_launchpad(self):
        """ Returns False if no launchpad, app version otherwise """
        # Device inquiry - check if we have the right launchpad.
        msg = mido.Message('sysex', data=[0x7E, 0x7F, 0x06, 0x01])
        self.p_out.send(msg)
        ret = self.p_in.receive()
        if not ret.type == 'sysex' or ret.data[0:7] != (126, 0, 6, 2, 0, 32, 41):
            return False
        launchpad_app_version = ret.data[-4:]
        return launchpad_app_version

    def set_programmer_mode(self):
        msg = mido.Message('sysex', data=LP_SYSEX_HEADER + [0x00, 0x11, 0x00, 0x00])
        self.p_out.send(msg)

        # check if that worked
        msg = mido.Message('sysex', data=LP_SYSEX_HEADER + [0x00])
        self.p_out.send(msg)
        ret = self.p_in.receive()
        if not ret.type == 'sysex' or ret.data != (0,32,41,2,14,0,17,0,0):
            return False
        return True

    def _setpixel(self, x, y, r, g, b):
        """ x=0 is left, y=0 is top. r, g, b are 0..255 
        When pixels outside the possible range are set, this fails silently (i.e. ignores)
        """
        type, pad = self.pixelmap.get((x, y), (None, None))
        if not pad:
            return
        r, g, b = round(r*self.brightness), round(g*self.brightness), round(b*self.brightness)
        color_number = colors.closest_color(r, g, b)
        if type == 'note':
            msg = mido.Message('note_on', channel=0, note=pad, velocity=color_number)
        elif type == 'cc':
            msg = mido.Message('control_change', channel=0, control=pad, value=color_number)
        self.p_out.send(msg)

    def setimage(self, image):
        """ image is a PIL image """
        # We use a trick: We set each pixel of the display every time regardless of the 
        # size of the image. When the image has no pixel for the given coordinate, we set
        # black.
        resize_ratio = min((self.pixelmap_max_x+1)/image.size[0], (self.pixelmap_max_y+1)/image.size[1])
        new_x = round(image.size[0] * resize_ratio)
        new_y = round(image.size[1] * resize_ratio)
        image_resized = image.resize((new_x, new_y), PIL.Image.Resampling.LANCZOS).convert('RGB')
        for x in range(0, self.pixelmap_max_x + 1):
            for y in range(0, self.pixelmap_max_y + 1):
                try:
                    r, g, b = image_resized.getpixel((x, y))
                except IndexError:
                    r, g, b = 0, 0, 0
                self._setpixel(x, y, r, g, b)

