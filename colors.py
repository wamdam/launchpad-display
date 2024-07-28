import math

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

def cv_to_ints(color_value):
    """ param: c27661
        returns: 194, 118, 97
    """
    return int(color_value[0:2], 16), int(color_value[2:4], 16), int(color_value[4:6], 16)


def color_distance(r1, g1, b1, r2, g2, b2):
  """Calculates the colour distance between two RGB colors.
  Returns:
    The colour distance between the two colors.
  """
  rmean = (r1 + r2) // 2
  r = r1 - r2
  g = g1 - g2
  b = b1 - b2
  return math.sqrt((((512 + rmean) * r * r) >> 8) + 4 * g * g + (((767 - rmean) * b * b) >> 8))


def closest_color(r, g, b):
    """ Returns the color number of the closest color on the launchpad
        Performance is about 12.000 calls per second on my cpu. 64 pads x 60fps = 3840, so this
        should be good enough.
    """
    min_distance_color_number = 0
    min_distance = 1e100  # Sorry, I don't know or have time to find the maximum.
    for color, color_number in COLOR_TABLE.items():
        distance = color_distance(r, g, b, *cv_to_ints(color))
        if distance < min_distance:
            min_distance = distance
            min_distance_color_number = color_number
    return min_distance_color_number


