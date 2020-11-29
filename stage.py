import random

class Stage(object):
    def __init__(self, width, height, file):
        self.width = width
        self.height = height
        self.tileSize = 40
        self.rowTiles = height // self.tileSize
        self.colTiles = width // self.tileSize
        self.generateTilesFromCSV(file)
        # print(self.rowTiles, self.colTiles)
        # print (self.tiles)

    def generateTilesFromCSV(self, file):
        self.tiles = set()
        CSV = readCSV(file)
        # print(CSV)
        # print(range(len(CSV)), range(len(CSV[0])))
        for row in range(len(CSV)):
            for col in range(len(CSV[0])):
                # print(CSV[row][col])
                if (CSV[row][col] == 0):
                    # print("Generating tile")
                    x = col * self.tileSize
                    y = row * self.tileSize
                    self.tiles.add(Square(x,y, self.tileSize))


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
    
    def inProximity(self, x, y, d):
        cx, cy = self.centerOfTile()
        return abs(cx - x) < d and abs(cy - y) < d

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
        return not (x2 >= x1 or x0 >= x3 or y2 >= y1 or y0 >= y3)

def readCSV(file):
    f = open(file, "r")
    lines = f.readlines()
    result = []
    for line in lines:
        result += [list(map(int, line.strip().split(",")))]
    f.close()
    return result
# print (readCSV("stages/1.csv"))





