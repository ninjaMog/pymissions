""" The main entrypoint for pymissions"""
# pylint: disable=I1101:c-extension-no-member
import ctypes
import sys
import pygame as pg
from draw import GameRenderer
from engine import GameState

# Default rendering settings
# Currently we scale this down if required for smaller resolutions
# Instead we should later consider rendering the viewport at a lower resolution
# And changing other sizes to match (e.g. hex_radius, font_size etc.)
VIEWPORT_PIXEL_SIZE = 3840, 2160
MAX_FPS = 60
HEX_RADIUS = 150


def main():
    """initialise and run the game!"""

    game_state = GameState()
    game_state.load_level()

    # Start up Pygame

    pg.init()  # pylint: disable=E1101:no-member

    # Take into account windows DPI scaling (Not sure what happens if you run this on Linux/Mac...)
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        print("Couldn't set DPIAware... We're probably not running on windows")

    # Initialise the display, and get the main surface
    main_surface = pg.display.set_mode(
        VIEWPORT_PIXEL_SIZE,
        pg.constants.SCALED | pg.constants.FULLSCREEN,
        vsync=1
    )

    # Give the window a title
    pg.display.set_caption("PYMISSIONS")

    clock = pg.time.Clock()
    running = True

    game_renderer = GameRenderer(
        main_surface, game_state, hex_radius=HEX_RADIUS, viewport_pixel_size=VIEWPORT_PIXEL_SIZE)

    # main game loop
    while running:
        for event in pg.event.get():
            if event.type == pg.constants.QUIT:
                running = False
            if event.type == pg.constants.KEYUP:
                if event.key == pg.constants.K_ESCAPE:
                    running = False

        # Draw the current game state
        game_renderer.draw()

        # flip() updates the entire display
        pg.display.flip()

        # limit FPS
        clock.tick(MAX_FPS)

    return pg.quit()  # pylint: disable=E1101:no-member


if __name__ == "__main__":
    sys.exit(main())
