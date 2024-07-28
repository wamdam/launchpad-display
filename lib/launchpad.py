import mido
import time
from . import colors
from . import launchpad_layout
import PIL
import curses
import atexit

LP_DEVICE_NAME = 'Launchpad Pro MK3:Launchpad Pro MK3 LPProMK3 MIDI 32:0'
LP_SYSEX_HEADER = [0x00, 0x20, 0x29, 0x02, 0x0E]

class Display():
    p_out = None
    p_in = None

    _received = None
    _received_messages = None
    _framebuffer = None
    _debug = False
    _resize = True

    def __init__(self, pixelmap, brightness=1.0, resize=True, debug=False):
        """ pixelmap is a dict of tuples: note-value (e.g. launchpad_layout.LAUNCHPAD_MK3_PRO) 
        """
        self.p_out = mido.open_output(LP_DEVICE_NAME)
        self.p_in = mido.open_input(LP_DEVICE_NAME)
        self._received_messages = []
        self.p_in.callback = self._receiver
        self.pixelmap = pixelmap
        self.pixelmap_max_x = max([d[0] for d in self.pixelmap.keys()])
        self.pixelmap_max_y = max([d[1] for d in self.pixelmap.keys()])
        self.brightness = brightness

        self._resize = resize
        self._debug = debug
        if self._debug:
            self._stdscr = curses.initscr()
            curses.start_color()
            curses.use_default_colors()
            for i in range(1, curses.COLORS):
                curses.init_pair(i, i, -1)
            curses.noecho()  # ?
            curses.cbreak()  # ?

            def exit_cleanup():
                curses.echo()
                curses.nocbreak()
                curses.endwin()
            atexit.register(exit_cleanup)

        _num_pixels = (self.pixelmap_max_x + 1) * (self.pixelmap_max_y + 1)
        self._framebuffer = [0] * _num_pixels

        self.clear()

        app_version = self.check_launchpad()
        if not app_version:
            raise ValueError("This is no launchpad: " + app_version)
        #print("Found Launchpad. App-Version: {}".format(app_version))
        if not self.set_programmer_mode():
            raise ValueError("Setting programmer mode didn't work")
        ##print("Set programmer mode")

    def _receiver(self, message):
        if message.type in ('clock', 'aftertouch'):
            return
        if message.type == 'note_on' and message.velocity == 0:
            return  # this is a note off
        print("Received: {}".format(message))
        self._received_messages.append(message)

    def receive(self):
        if not len(self._received_messages):
            time.sleep(.1)  # TODO this is ugly. Let's better block this simehow.
            return self.receive()
        else:
            message = self._received_messages.pop(0)
            print("Message buffer length: {}".format(len(self._received_messages)))
            return message

    def check_launchpad(self):
        """ Returns False if no launchpad, app version otherwise """
        # Device inquiry - check if we have the right launchpad.
        msg = mido.Message('sysex', data=[0x7E, 0x7F, 0x06, 0x01])
        self.p_out.send(msg)
        ret = self.receive()
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
        ret = self.receive()
        if not ret.type == 'sysex' or ret.data != (0,32,41,2,14,0,17,0,0):
            return False
        return True

    def _setpixel(self, x, y, r, g, b):
        """ x=0 is left, y=0 is top. r, g, b are 0..255 
        When pixels outside the possible range are set, this fails silently (i.e. ignores)
        """
        type, pad = self.pixelmap.get((x, y), (None, None))
        if pad:
            r, g, b = round(r*self.brightness), round(g*self.brightness), round(b*self.brightness)
            color_number_launchpad = colors.closest_color(r, g, b, colors.COLOR_TABLE_LAUNCHPAD)
            if type == 'note':
                msg = mido.Message('note_on', channel=0, note=pad, velocity=color_number_launchpad)
            elif type == 'cc':
                msg = mido.Message('control_change', channel=0, control=pad, value=color_number_launchpad)
            self.p_out.send(msg)
        offset = y * self.pixelmap_max_x + x

        if self._debug:
            color_number_terminal = colors.closest_color(r, g, b, colors.COLOR_TABLE_TERMINAL)
            self._framebuffer[offset] = color_number_terminal

    def _debug_framebuffer(self):
        for y in range(0, self.pixelmap_max_y + 1):
            for x in range(0, self.pixelmap_max_x + 1):
                offset = y * self.pixelmap_max_x + x
                color_number = self._framebuffer[offset]
                self._stdscr.addstr(y, x*2, '■■', curses.color_pair(color_number))
        self._stdscr.addstr(self.pixelmap_max_y + 2, 0, '', 0)  # set the cursor below
        self._stdscr.refresh()

    def clear(self):
        for x in range(self.pixelmap_max_x + 1):
            for y in range(self.pixelmap_max_y + 1):
                self._setpixel(x, y, 0, 0, 0)

    def setimage(self, image):
        """ image is a PIL image """
        # We use a trick: We set each pixel of the display every time regardless of the 
        # size of the image. When the image has no pixel for the given coordinate, we set
        # black.
        if self._resize:
            resize_ratio = min((self.pixelmap_max_x+1)/image.size[0], (self.pixelmap_max_y+1)/image.size[1])
            new_x = round(image.size[0] * resize_ratio)
            new_y = round(image.size[1] * resize_ratio)
            image_resized = image.resize((new_x, new_y), PIL.Image.Resampling.LANCZOS).convert('RGB')
        else:
            image_resized = image
        for x in range(0, self.pixelmap_max_x + 1):
            for y in range(0, self.pixelmap_max_y + 1):
                try:
                    r, g, b = image_resized.getpixel((x, y))
                except IndexError:
                    r, g, b = 0, 0, 0
                self._setpixel(x, y, r, g, b)

        if self._debug:
            self._debug_framebuffer()

