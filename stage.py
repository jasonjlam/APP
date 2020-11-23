import random

class Stage(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tileSize = 100
        self.rowTiles = height / self.tileSize
        self.colTiles = width / self.tileSize
        self.numTiles = 10
        self.generateTiles()

    def generateTiles(self):
        self.tiles = set()
        for i in range(self.numTiles):
            x = random.randint(0, self.colTiles - 1) * self.tileSize
            y = random.randint(0, self.rowTiles - 1) * self.tileSize
            self.tiles.add(Square(x, y, self.tileSize))
            print(f"Generated tile at ({x}, {y})")

class Tile(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def __repr__(self):
        return f"Tile at ({self.x}, {self.y})"
    def centerOfTile(self):
        return (self.x, self.y)
    
    def inProximity(self, x, y, r):
        cx, cy = self.centerOfTile()
        return ((x - cx) ** 2 + (y - cy) ** 2) < (r + self.size) ** 2

class Square(Tile):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.boundingBox = (x, y, x + size, y + size)
        self.size = size

    def centerOfTile(self):
        return (self.x + self.size / 2, self.y + self.size / 2)

    def isInTile(self, x, y):
        x0, y0, x1, y1 = self.boundingBox
        return (x > x0 and x < x1 and y > y0 and y < y1)

    def adjustBy(self, point, mode):
        x0, y0, x1, y1 = self.boundingBox
        # print (self.boundingBox)
        # print (point)
        x, y = point
        if (mode == "y"):
            if (abs(y- y0) < abs(y1 - y)):
                # print (y, y0)
                return y0 - y
            else:
                return y1 - y
        if (mode == "x"):
            if (abs(x - x0) < abs(x1 - x)):
                return x0 - x
            else:
                return x1 - x

