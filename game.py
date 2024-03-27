""" The main entrypoint for pymissions"""
# pylint: disable=I1101:c-extension-no-member
import sys
import pygame

# Default rendering settings
VIEWPORT_PIXEL_SIZE = (1280, 720)
MAX_FPS = 60

def main():
    """Run the game!"""
    pygame.init() #pylint: disable=E1101:no-member

    # Initialise the display and get a surface to draw on
    flags = pygame.constants.SCALED
    main_surface = pygame.display.set_mode(VIEWPORT_PIXEL_SIZE, flags, vsync=1)

    pygame.display.set_caption("PYMISSIONS")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                running = False

        # flip() updates the entire display
        pygame.display.flip()

        # limit FPS
        clock.tick(MAX_FPS)

    return pygame.quit() #pylint: disable=E1101:no-member

if __name__ == "__main__":
    sys.exit(main())
