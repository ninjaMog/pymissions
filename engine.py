"""
Classes responsible for game rules and state
"""
from hexy import HexMap
from tiles import STANDARD_TILES, GameTile


class GameState:
    """
    Store information about the current state of the game
    """

    def __init__(self):
        self.level = HexMap()

    def load_level(self):
        """
        Load a level, currently just loads a fixed level
        """
        # Represent a level in hex co-ordinates
        tiles = [
            GameTile((0, 0), "A", STANDARD_TILES[0]),
            GameTile((-1, 1), "B", STANDARD_TILES[1]),
            GameTile((0, 1), "C", STANDARD_TILES[2]),
            GameTile((-2, 2), "D", STANDARD_TILES[3]),
            GameTile((-1, 2), "E", STANDARD_TILES[4]),
            GameTile((0, 2), "F", STANDARD_TILES[5]),
            GameTile((-2, 3), "G", STANDARD_TILES[6]),
            GameTile((-1, 3), "H", STANDARD_TILES[7]),
            GameTile((-2, 4), "I", STANDARD_TILES[8])
        ]

        level = HexMap()
        for tile in tiles:
            level[tile.axial_coordinates] = [tile]

        self.level = level
