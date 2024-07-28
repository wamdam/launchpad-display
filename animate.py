import mido
import time

LP_DEVICE_NAME = 'Launchpad Pro MK3:Launchpad Pro MK3 LPProMK3 MIDI 32:0'
LP_SYSEX_HEADER = [0x00, 0x20, 0x29, 0x02, 0x0E]

""" A color table follows where the key is an rgb hex value as used in css
but without the leading #."""
COLOR_TABLE = {
        '616161': 0,
        'b3b3b3': 1,
        'dddddd': 2,
        'ffffff': 3,
        'ffb3b3': 4,
        'ff6161': 5,
        'dd6161': 6,
        'b36161': 7,
        'fff3d5': 8,
        'ffb361': 9,
        'dd8c61': 10,
        'b37661': 11,
        'ffeea1': 12,
        'ffff61': 13,
        'dddd61': 14,
        'b3b361': 15,
        'ddffa1': 16,
        'c2ff61': 17,
        'a1dd61': 18,
        '81b361': 19,
        'c2ffb3': 20,
        '61ff61': 21,
        '61dd61': 22,
        '61b361': 23,
        'c2ffc2': 24,
        '61ff8c': 25,
        '61dd76': 26,
        '61b36b': 27,
        'c2ffcc': 28,
        '61ffcc': 29,
        '61dda1': 30,
        '61b381': 31,
        'c2fff3': 32,
        '61ffe9': 33,
        '61ddc2': 34,
        '61b396': 35,
        'c2f3ff': 36,
        '61eeff': 37,
        '61c7dd': 38,
        '61a1b3': 39,
        'c2ddff': 40,
        '61c7ff': 41,
        '61a1dd': 42,
        '6181b3': 43,
        'a18cff': 44,
        '6161ff': 45,
        '6161dd': 46,
        '6161b3': 47,
        'ccb3ff': 48,
        'a161ff': 49,
        '8161dd': 50,
        '7661b3': 51,
        'ffb3ff': 52,
        'ff61ff': 53,
        'dd61dd': 54,
        'b361b3': 55,
        'ffb3d5': 56,
        'ff61c2': 57,
        'dd61a1': 58,
        'b3618c': 59,
        'ff7661': 60,
        'e9b361': 61,
        'ddc261': 62,
        'a1a161': 63,
        '61b361': 64,
        '61b38c': 65,
        '618cd5': 66,
        '6161ff': 67,
        '61b3b3': 68,
        '8c61f3': 69,
        'ccb3c2': 70,
        '8c7681': 71,
        'ff6161': 72,
        'f3ffa1': 73,
        'eefc61': 74,
        'ccff61': 75,
        '76dd61': 76,
        '61ffcc': 77,
        '61e9ff': 78,
        '61a1ff': 79,
        '8c61ff': 80,
        'cc61fc': 81,
        'ee8cdd': 82,
        'a17661': 83,
        'ffa161': 84,
        'ddf961': 85,
        'd5ff8c': 86,
        '61ff61': 87,
        'b3ffa1': 88,
        'ccfcd5': 89,
        'b3fff6': 90,
        'cce4ff': 91,
        'a1c2f6': 92,
        'd5c2f9': 93,
        'f98cff': 94,
        'ff61cc': 95,
        'ffc261': 96,
        'f3ee61': 97,
        'e4ff61': 98,
        'ddcc61': 99,
        'b3a161': 100,
        '61ba76': 101,
        '76c28c': 102,
        '8181a1': 103,
        '818ccc': 104,
        'ccaa81': 105,
        'dd6161': 106,
        'f9b3a1': 107,
        'f9ba76': 108,
        'fff38c': 109,
        'e9f9a1': 110,
        'd5ee76': 111,
        '8181a1': 112,
        'f9f9d5': 113,
        'ddfce4': 114,
        'e9e9ff': 115,
        'e4d5ff': 116,
        'b3b3b3': 117,
        'd5d5d5': 118,
        'f9ffff': 119,
        'e96161': 120,
        'aa6161': 121,
        '81f661': 122,
        '61b361': 123,
        'f3ee61': 124,
        'b3a161': 125,
        'eec261': 126,
        'c27661': 127,
    }

class Launchpad():
    p_out = None
    p_in = None

    def __init__(self):
        self.p_out = mido.open_output(LP_DEVICE_NAME)
        self.p_in = mido.open_input(LP_DEVICE_NAME)

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

    def pad(self):
        for i in range(0,127):
            # pads in the middle
            msg = mido.Message('note_on', channel=0, note=0x0b, velocity=i)
            self.p_out.send(msg)

            # pads in the ring
            msg = mido.Message('control_change', channel=0, control=0x0a, value=i)
            self.p_out.send(msg)
            time.sleep(.1)



lp = Launchpad()
app_version = lp.check_launchpad()
if not app_version:
    raise ValueError("This is no launchpad")
print("Found Launchpad. App-Version: {}".format(app_version))
if not lp.set_programmer_mode():
    raise ValueError("Setting programmer mode didn't work")
print("Set programmer mode")

lp.pad()


#for msg in lp.p_in:
#   print(msg)
