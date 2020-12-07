# Has base class Stage, which defines each "zone" displayed on screen.
# Subclasses Stage1, Stage2... represent each stage and their individual
# assets/entities.
# Stages import much of their tileset from /stages/(n).csv
# These files are created with Tiled

from random import *
from tiles import *
from entities import *
from bosses import *

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')

def addBumps(textureMap):
    i = 2
    while (i < 28):
        width = randint(3, 5)
        height = randint(-1, 2)
        for x in range(i, min(28, i + width)):
            textureMap[x] += height
        i += width

class Stage(object):
    def __init__(self, width, height, startY, endY, num = 1):
        self.width = width
        self.height = height
        self.tileSize = 40
        self.numRows = height // self.tileSize
        self.numCols = width // self.tileSize
        self.startY = startY
        self.num = 1
        self.endY = endY
        self.tiles = []
        self.stage = [([0] * self.numCols) for row in range(self.numRows)]
        self.movingTiles = []
        self.entities = []
        self.boss = None
        self.generateStage()
        self.stageToTiles()

    def generateStage(self):
        self.stage[self.startY - 2][1] = 3
        terrainMap = []
        self.stage[self.startY][0] = 1
        self.stage[self.startY][1] = 1
        self.stage[self.endY][self.numCols - 2] = 1
        self.stage[self.endY][self.numCols - 1] = 1
        # self.generateSlope()
        self.generatePit()
        # print2dList(self.stage)

    def generatePit(self):
        for x in range(2, self.numCols - 2):
            self.stage[self.numRows - 1][x] = 2
        for y in range(self.startY, self.numRows):
            self.stage[y][1] = 1
        for y in range(self.endY, self.numRows):
            self.stage[y][self.numCols - 2] = 1
        self.stage[10][20] = 5
    def generateSlope(self):
        slope = (self.endY - self.startY) / (self.numCols)
        terrainMap = [self.startY, self.startY]
        for i in range(2, self.numCols - 2):
            y = int(round(self.startY + slope * i, 0))
            terrainMap += [y]
        for i in range(2):
            terrainMap += [self.endY]
        addBumps(terrainMap)
        for i in range(1, len(terrainMap) - 2):
            if (terrainMap[i] != terrainMap[i + 1]):
                y0 = terrainMap[i]
                y1 = terrainMap[i + 1]
                if (y0 > y1):
                    for y in range(y1, y0):
                        self.stage[y][i] = 1
                elif (y0 < y1):
                    for y in range(y0, y1 + 1):
                        self.stage[y][i] = 1
        for i in range(len(terrainMap)):
            self.stage[terrainMap[i]][i] = 1



    def stageToTiles(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                # print(self.numRows, self.numCols)
                x = col * self.tileSize
                y = row * self.tileSize
                if (self.stage[row][col] == 1):
                    self.tiles.append(Square(x, y, self.tileSize))
                elif (self.stage[row][col] == 2):
                    self.entities.append(UpwardSpike(x, y, self.tileSize))
                elif (self.stage[row][col] == 3):
                    self.tiles.append(Save(x, y, 20, self))
                elif (self.stage[row][col] == 4):
                    self.movingTiles.append(VanishingTile(
                        x, y, self.tileSize, self))
                elif (self.stage[row][col] == 5):
                    self.tiles.append(FireBar(x, y, self.tileSize, 200, 50, -1, 
                        self))

    def generateNewStage(self):
        startY = self.endY
        endY = randint(7, 17)
        print(startY, endY)
        return Stage(self.width, self.height, startY, endY, self.num + 1)


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





class Stage2(Stage):
    def __init__(self, width, height):
        super().__init__(width, height, "stages/2.csv")
        self.entrance = "blocked"
        self.exit = "right"
        self.boss = Haunter(20 * 40, 3 * 40, self)

    def addTiles(self):
        for i in range(9, 30):
            self.tiles.append(Square(40 * i, 15 * self.tileSize, self.tileSize))
        




