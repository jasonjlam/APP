import random

class Stage(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tileSize = 50
        self.rowTiles = height / self.tileSize
        self.colTiles = width / self.tileSize
        self.numTiles = 20
        self.generateTiles()

    def generateTiles(self):
        self.tiles = set()
        for i in range(self.numTiles):
            x = random.randint(0, self.colTiles - 1) * self.tileSize
            y = random.randint(0, self.rowTiles - 1) * self.tileSize
            self.tiles.add(Square(x, y, self.tileSize))
            print(f"Generated tile at ({x}, {y})")
        for i in range(self.width // self.tileSize):
            x = i * self.tileSize
            y = self.height - self.tileSize
            self.tiles.add(Square(x, y, self.tileSize))

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

    def boxesIntersect(self, boundingBox):
        # print(self.boundingBox)
        x0, y0, x1, y1 = self.boundingBox
        x2, y2, x3, y3 = boundingBox
        # print(x0, y0, x1, y1, x2, y2, x3, y3)
        # if (not (x2 >= x1 or x0 >= x3 or y2 >= y1 or y0 >= y3)):
            # print("Intersect")
        return not (x2 >= x1 or x0 >= x3 or y2 >= y1 or y0 >= y3)

def boxesCheck(x0, y0, x1, y1, x2, y2, x3, y3):
    return not (x2 >= x1 or x0 >= x3 or y2 >= y1 or y0 >= y3)
print (boxesCheck(200, 300, 400, 500, 371.0, 463.0, 416.0, 464.0))
print (boxesCheck(200, 300, 400, 500, 370.0, 465.0, 394.0, 501.0))
print (boxesCheck(200, 300, 400, 500, 395.0, 465.0, 417.0, 501.0))
print (boxesCheck(200, 300, 400, 500, 371.0, 501.0, 416.0, 505.0))



