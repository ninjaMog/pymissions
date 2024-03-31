"""
Classes responsible for rendering the game
"""
# pylint: disable=I1101:c-extension-no-member
import hexy as hx
import numpy as np
import pygame as pg
from engine import GameState

FONT_SIZE = 24


class GameRenderer:
    """
    Class responsible for rendering the game state to screen
    """

    def __init__(self, game_surface: pg.Surface, game_state: GameState,
                 hex_radius, viewport_pixel_size):
        self.surface = game_surface
        self.game_state = game_state
        self.hex_radius = hex_radius
        self.viewport_pixel_size = viewport_pixel_size

        # Calculate pixel calcuations for objects in current state
        for tile in game_state.level.values():
            tile.position = hx.axial_to_pixel(
                tile.axial_coordinates, hex_radius)

        # Setup images & related calculations
        self.background_image = pg.image.load("./media/images/starfield.png")
        self.hex_image = self.get_hex_image()

        # offset to draw the tiles at
        self.map_offset = self.get_map_offset()
        # default font to use

        # create a font
        pg.font.init()
        self.font = pg.font.SysFont("monospace", FONT_SIZE, True)

    def get_hex_image(self):
        """
        Return an image representing a basic game tile
        """
        image = self.make_hex_surface((255, 255, 255), self.hex_radius)
        image = self.apply_hex_background(image)
        return image

    def draw(self):
        """
        Draws current game state

        Minimize calculations in this method, as it will be called every frame
        """

        # Redraw the background
        self.surface.blit(self.background_image, (0, 0))

        image_center = [self.hex_image.get_width(
        ) / 2, self.hex_image.get_height() / 2]

        # Draw the hexes
        for tile in self.game_state.level.values():
            draw_position = tile.position[0] - image_center + self.map_offset
            self.surface.blit(self.hex_image, draw_position)

        # draw IDs on the hexes
        for tile in self.game_state.level.values():
            text = self.font.render(str(tile.tile_id), False, (0, 0, 0))
            text.set_alpha(160)
            text_pos = tile.position[0] + self.map_offset
            text_pos -= (text.get_width() / 2, text.get_height() / 2)
            self.surface.blit(text, text_pos)

    def get_map_offset(self):
        """
        Calculate how far tiles should be shifted on the X and Y coordinates based on map shape
        """
        # We want half main surface dimension (screen) + half dimension of map
        x_values = [tile.position[0][0]
                    for tile in self.game_state.level.values()]
        y_values = [tile.position[0][1]
                    for tile in self.game_state.level.values()]

        offset = [
            int((self.viewport_pixel_size[0] - (max(x_values) -
                                                min(x_values)) + self.hex_image.get_width()) / 2),
            int((self.viewport_pixel_size[1] - (max(y_values) -
                                                min(y_values))) / 2)
        ]

        return offset

    def make_hex_surface(self, color, radius,
                         border_color=(100, 100, 100), border=True, hollow=False):
        """
        Draws a hexagon with gray borders on a pygame surface.
        :param color: The fill color of the hexagon.
        :param radius: The radius (from center to any corner) of the hexagon.
        :param border_color: Color of the border.
        :param border: Draws border if True.
        :param hollow: Does not fill hex with color if True.
        :return: A pygame surface with a hexagon drawn on it
        """
        # This functionis a simplified version of the functionn in the Hexy module examples
        # I also tweaked it as I think it was calculating the surface size wrong
        # Which caused issues when trying to apply a background image to the polygon
        # https://github.com/RedFT/HexyExamples/blob/e1c52067894eb989d1d5ec6854cd0cde7106289d/example_hex.py#L7

        # Get the angels of each of the points of the hexagon
        angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])

        # Get cordinates of these pointse
        points = np.round(np.vstack([
            radius * np.cos(angles_in_radians), radius *
            np.sin(angles_in_radians)
        ]).T)

        # Get minimum and maximum locations of the points of the hex
        sorted_x = sorted(points[:, 0])
        sorted_y = sorted(points[:, 1])
        surf_size = np.array(
            [sorted_x[-1] - sorted_x[0], sorted_y[-1] - sorted_y[0]]
        )
        # calculate the center point of the surface
        surf_center = surf_size / 2

        surface = pg.Surface(surf_size.tolist())
        surface.set_colorkey((0, 0, 0))

        # Set alpha if color has 4th coordinate.
        if len(color) >= 4:
            surface.set_alpha(color[-1])

        # fill if not hollow.
        if not hollow:
            pg.draw.polygon(surface, color, (points + surf_center).tolist(), 0)

        # if border is true or hollow is true draw border.
        if border or hollow:
            pg.draw.lines(surface, border_color, True,
                          (points + surf_center).tolist(), 1)

        return surface

    def apply_hex_background(self, image: pg.Surface):
        """
        Applys a background image to the provided image
        """
        bg_image = pg.image.load(
            "media/images/ground_tile_lowres.jpg")

        # The images aren't the same size, so we want to center the background image
        tile_offset = (
            (image.get_width() - bg_image.get_width()) / 2,
            (image.get_height() - bg_image.get_width()) / 2
        )

        image.blit(bg_image, tile_offset,
                   special_flags=pg.constants.BLEND_MULT)

        return image
