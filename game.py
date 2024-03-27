""" The main entrypoint for pymissions"""
# pylint: disable=I1101:c-extension-no-member
import sys
import pygame as pg
import numpy as np

# Default rendering settings
VIEWPORT_PIXEL_SIZE = (1280, 720)
MAX_FPS = 60

# This is taken directly from the Hexy module examples
# https://github.com/RedFT/HexyExamples/blob/e1c52067894eb989d1d5ec6854cd0cde7106289d/example_hex.py#L7
def make_hex_surface(color, radius, border_color=(100, 100, 100), border=True, hollow=False):
    """
    Draws a hexagon with gray borders on a pygame surface.
    :param color: The fill color of the hexagon.
    :param radius: The radius (from center to any corner) of the hexagon.
    :param border_color: Color of the border.
    :param border: Draws border if True.
    :param hollow: Does not fill hex with color if True.
    :return: A pygame surface with a hexagon drawn on it
    """
    angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
    x = radius * np.cos(angles_in_radians)
    y = radius * np.sin(angles_in_radians)
    points = np.round(np.vstack([x, y]).T)

    sorted_x = sorted(points[:, 0])
    sorted_y = sorted(points[:, 1])
    minx = sorted_x[0]
    maxx = sorted_x[-1]
    miny = sorted_y[0]
    maxy = sorted_y[-1]

    sorted_idxs = np.lexsort((points[:, 0], points[:, 1]))

    surf_size = np.array((maxx - minx, maxy - miny)) * 2 + 1
    center = surf_size / 2
    surface = pg.Surface(surf_size.tolist())
    surface.set_colorkey((0, 0, 0))

    # Set alpha if color has 4th coordinate.
    if len(color) >= 4:
        surface.set_alpha(color[-1])

    # fill if not hollow.
    if not hollow:
        pg.draw.polygon(surface, color, (points + center).tolist(), 0)


    points[sorted_idxs[-1:-4:-1]] += [0, 1]
    # if border is true or hollow is true draw border.
    if border or hollow:
        pg.draw.lines(surface, border_color, True, (points + center).tolist(), 1)

    return surface

def main():
    """Run the game!"""
    pg.init() #pylint: disable=E1101:no-member

    # Initialise the display and get a surface to draw on
    flags = pg.constants.SCALED
    main_surface = pg.display.set_mode(VIEWPORT_PIXEL_SIZE, flags, vsync=1)

    pg.display.set_caption("PYMISSIONS")
    clock = pg.time.Clock()
    running = True

    # draw a hex
    image = make_hex_surface((255, 255, 255), 20)
    main_surface.blit(image, [0, 0])

    while running:
        for event in pg.event.get():
            if event.type == pg.constants.QUIT:
                running = False

        # flip() updates the entire display
        pg.display.flip()

        # limit FPS
        clock.tick(MAX_FPS)

    return pg.quit() #pylint: disable=E1101:no-member

if __name__ == "__main__":
    sys.exit(main())
