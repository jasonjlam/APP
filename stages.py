# Has base class Stage, which defines each "zone" displayed on screen.
# Subclasses Stage1, Stage2... represent each stage and their individual
# assets/entities.
# Stages import much of their tileset from /stages/(n).csv
# These files are created with Tiled

from random import *
from tiles import *
from entities import *
from bosses import *

def addBumps(textureMap):
    i = 2
    while (i < 38):
        width = randint(4, 6)
        height = randint(-1, 1)
        for x in range(i, min(38, i + width)):
            textureMap[x] += height
        i += width + randint(0, 2)

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
        self.generateTraps()
        self.stageToTiles()

    def generateStage(self):
        self.stage[self.startY - 2][1] = 3
        terrainMap = []
        self.stage[self.startY][0] = 1
        self.stage[self.startY][1] = 1
        self.stage[self.endY][self.numCols - 2] = 1
        self.stage[self.endY][self.numCols - 1] = 1
        pitChance = 0.3 + self.num / 30
        if (random() < pitChance):
            self.generatePit()
        else:
            self.generateSlope()
        # print2dList(self.stage)

    def generatePit(self):
        for x in range(2, self.numCols - 2):
            self.stage[self.numRows - 1][x] = 2
        for y in range(self.startY, self.numRows):
            self.stage[y][1] = 1
        for y in range(self.endY, self.numRows):
            self.stage[y][self.numCols - 2] = 1
        x = 4
        y = self.startY
        while (x < self.numCols - 4):
            yOffset = 0
            while (abs(yOffset) < 3):
                yOffset = randint(-4, 4)
                print(yOffset)
            y += yOffset
            if (y < 6):
                y = 6
            if (y > 18):
                y = 18
            x += randint(-1, 2)
            width = randint(3,4)
            for extraX in range(width):
                if (x + extraX < self.numCols - 2):
                    self.stage[y][x + extraX] = 1
            x += width
        if (y - self.endY) > 4:
            while (y > self.endY):
                self.stage[y][self.numCols -3] = 1
                y += randint(-4, -3)

    def generateSlope(self):
        slope = (self.endY - self.startY) / (self.numCols)
        terrainMap = [self.startY, self.startY]
        for i in range(2, self.numCols - 2):
            y = int(round(self.startY + slope * i, 0))
            terrainMap += [y]
        for i in range(2):
            terrainMap += [self.endY]
        yMin = self.startY
        while (yMin > 3):
            x = 2
            while (x < self.numCols - 4):
                yOffset = randint(-7, -4)
                y = terrainMap[x] + yOffset + yMin - self.startY
                print(terrainMap[x], y)
                if (y < 2):
                    y = 2
                if (y > 18):
                    y = 18
                x += randint(2, 4)
                width = randint(2, 8)
                for extraX in range(width):
                    if (x + extraX < self.numCols - 2):
                        self.stage[y][x + extraX] = 1
                x += width
            yMin -= randint(3, 4)
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

    def generateTraps(self):
        trapScore = 10 + (self.num) / 3
        currentScore = 0
        traps = {"FireBar": 0, "Spike": 0, "Laser": 0}
        iterations = 0
        while (currentScore < trapScore and iterations < 1000):
            while (iterations < 1000):
                iterations += 1
                row = randint(2, self.numRows - 2)
                col = randint(2, self.numCols - 2)
                if (self.stage[row][col] == 1):
                    rng = random()
                    if (not self.checkAdjacentTraps(row, col)):
                        if (rng < 0.2 and traps["Laser"] < 3):
                            if (self.generateLaser()):
                                currentScore += 2
                                traps["Laser"] += 1
                        elif (rng < 0.4 and traps["FireBar"] < 3):
                            self.stage[row][col] = 5
                            currentScore += 2
                            traps["FireBar"] += 1
                        elif (rng < 1):
                            self.stage[row - 1][col] = 2
                            currentScore += 1
                            traps["Spike"] += 1
                        break

    def generateLaser(self):
        iterations = 0
        while (iterations < 100):
            row = randint(4, self.numRows - 4)
            col = randint(2, self.numCols - 2)
            iterations += 1
            if (self.stage[row][col] == 1):
                if (self.stage[row + 1][col] != 0
                    or self.stage[row + 2][col] != 0):
                    print("blocked")
                    continue
                for i in range(row + 3, self.numRows - 1):
                    if (self.stage[i][col] != 0):
                        self.stage[row + 1][col] = 6
                        return True
        return False
    def checkAdjacentTraps(self, row, col):
        for r in range(-2, 2):
            for c in range(-2, 2):
                if (r != 0 or c != 0):
                    if (self.stage[row + r][col + c] in [2, 5]):
                        return True
        else:
            return False
                    
        

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
                    self.tiles.append(FireBar(x, y, self.tileSize, 
                    randint(100, 200) + self.num, randint(60, 100) - self.num / 2,
                    [-1, 1][randint(0,1)], self))
                elif (self.stage[row][col] == 6):
                    height = 40
                    for i in range(1, self.numRows - 1 - row):
                        if (self.stage[row + i][col] != 0):
                            height = i * self.tileSize
                            print(i, self.stage[i][col], height)
                            break
                    self.entities.append(VerticalLaser(x, y, 
                    height, randint(70, 100) - self.num / 2))


    def generateNewStage(self):
        startY = self.endY
        endY = randint(10, 17)
        return Stage(self.width, self.height, startY, endY, self.num + 1)

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
        self.boss = Haunter(30 * 40, 3 * 40, self)

    def addTiles(self):
        for i in range(9, 30):
            self.tiles.append(Square(40 * i, 15 * self.tileSize, self.tileSize))
        




