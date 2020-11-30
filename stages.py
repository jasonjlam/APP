# Has base class Stage, which defines each "zone" displayed on screen.
# Subclasses Stage1, Stage2... represent each stage and their individual
# assets/entities.
# Stages import much of their tileset from /stages/(n).csv
# These files are created with Tiled

import random
from tiles import *

class Stage(object):
    def __init__(self, width, height, file):
        self.width = width
        self.height = height
        self.tileSize = 40
        self.rowTiles = height // self.tileSize
        self.colTiles = width // self.tileSize
        self.generateTilesFromCSV(file)
        self.movingTiles = []
        # print(self.rowTiles, self.colTiles)
        # print (self.tiles)

    def generateTilesFromCSV(self, file):
        self.tiles = []
        CSV = readCSV(file)
        # print(CSV)
        # print(range(len(CSV)), range(len(CSV[0])))
        for row in range(len(CSV)):
            for col in range(len(CSV[row])):
                # print(CSV[row][col])
                if (CSV[row][col] == 0):
                    # print("Generating tile")
                    x = col * self.tileSize
                    y = row * self.tileSize
                    self.tiles.append(Square(x,y, self.tileSize))

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

    def getTiles(self):
        return self.tiles + self.movingTiles

def createStage(stage, width, height):
    w = width
    h = height
    stages = {1: Stage1(w, h), 2:Stage2(w, h), 3: Stage3(w,h), 4: Stage4(w,h),
            5: Stage5(w, h)}
    return stages[stage]

def readCSV(file):
    f = open(file, "r")
    lines = f.readlines()
    result = []
    for line in lines:
        result += [list(map(int, line.strip().split(",")))]
    f.close()
    return result

class Stage1(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/1.csv")
        self.entrance = "left"
        self.exit = "right"
        self.generateAdditionalTiles()

    def generateAdditionalTiles(self):
        platform1 = MovingPlatform(18 * 40, 6 * 40, 18 * 40, 15 * 40, 60, 
                                    0, 4)
        self.movingTiles.append(platform1)

class Stage2(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/2.csv")
        self.entrance = "left"
        self.exit = "right"

class Stage3(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/3.csv")
        self.entrance = "left"
        self.exit = "top"

class Stage4(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/4.csv")
        self.entrance = "bot"
        self.exit = "top"

class Stage5(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/5.csv")
        self.entrance = "bot"
        self.exit = "top"
# print (readCSV("stages/1.csv"))





