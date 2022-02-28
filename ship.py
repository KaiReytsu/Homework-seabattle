from enum import Enum

class ShipType(Enum):
    single_deck = 1
    double_deck = 2
    triple_deck = 3
    quad_deck = 4

class ShipOrientation(Enum):
    horizontally = 0
    vertically = 1

class Ship:
    def __init__(self, deck_type, orientation, x, y):
        self.type = deck_type
        self.orientation = orientation
        self.x = x
        self.y = y