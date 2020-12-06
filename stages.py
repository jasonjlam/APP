# Has base class Stage, which defines each "zone" displayed on screen.
# Subclasses Stage1, Stage2... represent each stage and their individual
# assets/entities.
# Stages import much of their tileset from /stages/(n).csv
# These files are created with Tiled

import random
from tiles import *
from entities import *
from bosses import *

class Stage(object):
    def __init__(self, width, height, file):
        self.width = width
        self.height = height
        self.tileSize = 40
        self.rowTiles = height // self.tileSize
        self.colTiles = width // self.tileSize
        self.movingTiles = []
        self.entities = []
        self.generateTilesFromCSV(file)
        self.generateMovingTiles()
        self.generateEntities()
        self.boss = None
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
                x = col * self.tileSize
                y = row * self.tileSize
                if (CSV[row][col] == 0):
                    # print("Generating tile")
                    self.tiles.append(Square(x, y, self.tileSize))
                elif (CSV[row][col] == 1):
                    self.entities.append(UpwardSpike(x, y, self.tileSize))
                elif (CSV[row][col] == 2):
                    self.tiles.append(Save(x, y, 20, self))
                elif (CSV[row][col] == 3):
                    self.movingTiles.append(VanishingTile(
                        x, y, self.tileSize, self))

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

    def generateMovingTiles(self):
        pass

    def generateEntities(self):
        pass

    def getTiles(self):
        return self.tiles + self.movingTiles

    def getEntities(self):
        if (self.boss != None):
            return [self.boss] + self.entities
        else:
            return self.entities

def createStage(stage, width, height):
    w = width
    h = height
    stages = {1: Stage1(w, h), 2:Stage2(w, h), 3: Stage3(w,h), 4: Stage4(w,h),
            5: Stage5(w, h), 6: Stage6(w,h), 7: Stage7(w,h)}
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

    def generateMovingTiles(self):
        platform1 = MovingPlatform(18 * 40, 6 * 40, 18 * 40, 15 * 40, 120, 
                                    0, 4)
        self.movingTiles.append(platform1)

class Stage2(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/2.csv")
        self.entrance = "blocked"
        self.exit = "right"
        self.boss = Haunter(20 * 40, 3 * 40, self)

    def addTiles(self):
        for i in range(9, 30):
            self.tiles.append(Square(40 * i, 15 * self.tileSize, self.tileSize))
        
class Stage3(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/3.csv")
        self.entrance = "blocked"
        self.exit = "top"

    def generateMovingTiles(self):
        platform1 = MovingPlatform(1 * 40, 11 * 40, 11 * 40, 11 * 40, 80, 
                                4, 0)
        self.movingTiles.append(platform1)

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

class Stage6(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/6.csv")
        self.entrance = "bot"
        self.exit = "left"

class Stage7(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/7.csv")
        self.entrance = "right"
        self.exit = "left"

    def generateMovingTiles(self):
        platform1 = MovingPlatform(0, 16 * 40, 28 * 40, 16 * 40, 80, 8, 0)
        self.movingTiles.append(platform1)





