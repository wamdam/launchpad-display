from lib import launchpad
from lib import launchpad_layout
from PIL import Image, ImageFont, ImageDraw
import time
import random

def game_of_life(width, height, initial_grid):
    """
    Yields successive generations of the Game of Life on a toroidal grid.

    Args:
        width: Width of the grid.
        height: Height of the grid.
        initial_grid: A 2D list representing the initial state of the grid.

    Yields:
        A 2D list representing the grid in the next generation.
    """

    def count_neighbors(x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                count += grid[(x + i + width) % width][(y + j + height) % height]
        return count

    grid = initial_grid

    while True:
        new_grid = [[0] * width for _ in range(height)]
        for x in range(width):
            for y in range(height):
                neighbors = count_neighbors(x, y)
                if grid[x][y] == 1:
                    new_grid[x][y] = 1 if neighbors in (2, 3) else 0
                else:
                    new_grid[x][y] = 1 if neighbors == 3 else 0
        grid = new_grid
        yield grid


def random_grid(width, height):
    grid = []
    for y in range(height+1):
        grid_line = []
        for x in range(width+1):
            grid_line.append(random.randint(0, 1))
        grid.append(grid_line)
    return grid

def random_color():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

#framerate = 10  # 120bpm
framerate = 10.42  # 125bpm


display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO, brightness=1.0, scale=False, debug=True)
#display = launchpad.Display(launchpad_layout.LAUNCHPAD_MK3_PRO_AMBIENT, brightness=2.0)

width = display.pixelmap_max_x + 1
height = display.pixelmap_max_y + 1
display_image = Image.new('RGB', (width, height), color=0x000000)
grid_1 = None
grid_2 = None

while True:
    initial_grid = random_grid(width, height)
    color = random_color()
    generation = 0
    for grid in game_of_life(8, 8, initial_grid):
        t1 = time.time()
        for x in range(0, 8):
            for y in range(0, 8):
                if grid[x][y] == 1:
                    display_image.putpixel((x, y), color)
                else:
                    display_image.putpixel((x, y), (0, 0, 0))
        if max(grid) == [0] * width or grid == grid_1 or grid == grid_2 or generation > 100:
            time.sleep(.5)
            #print("New!")
            break
        grid_2 = grid_1
        grid_1 = grid
        display.setimage(display_image)
        generation += 1
        time.sleep(1/framerate - (time.time() - t1))
