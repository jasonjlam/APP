import random

class Stage(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tileSize = 40
        self.rowTiles = height / tileSize
        self.colTiles = width / tileSize
        self.tiles = set()

    def generateTiles(self):
        pass

class Tile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def centerOfTile(self):
        return (self.x, self.y)

class Square(Tile):
    def __init__(self, x, y, size):
        self.boundingBox = (x, y, x + size, x - size)

    def centerOfTile(self):
        return (x + size / 2, y + size / 2)

    def isInTile(self, x, y):
        x0, y0, x1, y1 = self.boundingBox
        return (x > x0 and x < x1 and y > y0 and y < y1)