"""
Contains classes and constants related to game tiles
"""
from hexy import HexTile


class Tile():
    """
    Represents a basic tile, and it's properties (i.e. doors & vents)
    """

    def __init__(self, tile_id: int, doors: list[int], has_vent: bool = False):
        self.tile_id = tile_id
        self.doors = doors
        self.has_vent = has_vent

    def has_door(self, i):
        """
        Returns whether a door existins in direcition (0-indexed clockwise from top)
        """
        return i in self.doors


class GameTile(HexTile):
    """
    Extended version of HexTile that includes tile info like doors & vents
    """

    def __init__(self, axial_coordinates, tile_id, tile: Tile):
        # We don't really want these classes to be aware of display info like hex radius,
        # so set a default here, we'll cacluate real screeen position in the display routines
        super().__init__(axial_coordinates, 1, tile_id)
        self.gametile = tile


# Basic Tiles - Doors represented 0-indexed clockwise from top edge
STANDARD_TILES = [
    Tile(15, []),
    Tile(16, []),
    Tile(17, [], True),
    Tile(18, []),
    Tile(19, [], True),
    Tile(20, []),
    Tile(21, [0], True),
    Tile(22, [1]),
    Tile(23, [5]),
    Tile(24, [2]),
    Tile(25, [4]),
    Tile(26, [3]),
    Tile(27, [0, 5]),
    Tile(28, [2, 5]),
    Tile(29, [2, 3]),
    Tile(30, [1, 2]),
    Tile(31, [1, 3]),
    Tile(32, [1, 4]),
    Tile(33, [0, 1]),
    Tile(34, [3, 4]),
    Tile(35, [0, 2], True),
    Tile(36, [4, 5]),
    Tile(37, [0, 5]),
    Tile(38, [3, 5]),
    Tile(39, [2, 4]),
    Tile(40, [0, 4]),
    Tile(41, [0, 3], True),
    Tile(42, [0, 2, 4], True),
    Tile(43, [1, 2, 4]),
    Tile(44, [2, 4, 5]),
    Tile(45, [1, 3, 5]),
    Tile(46, [1, 3, 4]),
    Tile(47, [0, 1, 4])
]

# Scenario Tiles
