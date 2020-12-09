# Has base class Stage, which defines each "zone" displayed on screen.
# Also has class Platform, which is used to randomly generate platforms
# Also a special stage for the boss

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
        self.platforms = []
        self.width = width
        self.height = height
        self.tileSize = 40
        self.numRows = height // self.tileSize
        self.numCols = width // self.tileSize
        self.startY = startY
        self.num = num
        self.endY = endY
        self.tiles = []
        self.stage = [([0] * self.numCols) for row in range(self.numRows)]
        self.movingTiles = []
        self.entities = []
        self.boss = None
        self.generateStage()
        self.stageToTiles()

    def generateStage(self):
        self.stage[self.endY - 2][self.numCols - 1] = 3
        terrainMap = []
        self.stage[self.startY][0] = 1
        self.stage[self.startY][1] = 1
        self.stage[self.endY][self.numCols - 2] = 1
        self.stage[self.endY][self.numCols - 1] = 1
        pitChance = 0.3 + self.num / 50
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
            y += yOffset
            if (y < 3):
                y = 3
            if (y > 18):
                y = 18
            x += randint(-1, 2)
            width = min(randint(3,5), max(2, self.numCols - 3 - x))
            self.platforms += [Platform(x * self.tileSize, y * self.tileSize,
                width * self.tileSize, self.tileSize)]
            x += width
        for platform in self.platforms:
            platform.toStage(self)
        if (y - self.endY) > 4:
            while (y > self.endY):
                self.stage[y][self.numCols - 3] = 1
                y += randint(-4, -3)
        self.generatePlatforms(0.07, 17)
        self.generateTraps(3 + self.num)

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
                    for y in range(y1, y0 + 1):
                        self.stage[y][i] = 1
                elif (y0 < y1):
                    for y in range(y0, y1 + 1):
                        self.stage[y][i] = 1
        for i in range(len(terrainMap)):
            self.stage[terrainMap[i]][i] = 1
        self.generatePlatforms(0.15, max(self.startY, self.endY))
        self.generateTraps(6 + self.num * 1.5)

    def generatePlatforms(self, platformChance, y):
        for row in range(2, y):
            for col in range(2, self.numCols - 2):
                if (random() < platformChance):
                    # print("platform", row, col)
                    width = min(randint(2,11), max(2, 
                        self.numCols - col - 3))*self.tileSize
                    # print(width // self.tileSize)
                    platform = (Platform(col * self.tileSize, 
                    row * self.tileSize, width, self.tileSize))
                    if (platform.isValid(self.stage)):
                        # print("valid platform")
                        self.platforms.append(platform)
                        platform.toStage(self)


    def generateTraps(self, trapScore):
        currentScore = 0
        traps = {"FireBar": 0, "Spike": 0, "Laser": 0, "DartTrap": 0}
        iterations = 0
        while (currentScore < trapScore and iterations < 1000):
            while (iterations < 1000):
                iterations += 1
                row = randint(2, self.numRows - 2)
                col = randint(2, self.numCols - 2)
                if (self.stage[row][col] == 1):
                    rng = random()
                    if (not self.checkAdjacentTraps(row, col)):
                        if (rng < 0.2 and traps["Laser"] < 5):
                            if (self.generateLaser()):
                                currentScore += 2
                                traps["Laser"] += 1
                        elif (rng < 0.4 and traps["FireBar"] < 5):
                            self.stage[row][col] = 5
                            currentScore += 3
                            traps["FireBar"] += 1
                        elif (rng < 0.6 and traps["DartTrap"] < 4):
                            currentScore += 2
                            self.stage[row][col] = 7
                            traps["DartTrap"] += 1
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
                    continue
                for i in range(row + 3, self.numRows - 1):
                    if (self.stage[i][col] not in [-1, 0]):
                        self.stage[row + 1][col] = 6
                        return True
        return False

    def checkAdjacentTraps(self, row, col):
        if (row + 3 > self.numRows or col + 3 > self.numCols):
            return False
        for r in range(-2, 3):
            for c in range(-2, 3):
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
                    randint(100, 200) + self.num, randint(90, 120) - self.num / 2,
                    [-1, 1][randint(0,1)], self))
                elif (self.stage[row][col] == 6):
                    height = 40
                    for i in range(1, self.numRows - 1 - row):
                        if (self.stage[row + i][col] not in [-1, 0]):
                            height = i * self.tileSize
                            break
                    self.entities.append(VerticalLaser(x, y, 
                    height, randint(70, 100) - self.num))
                elif (self.stage[row][col] == 7):
                    platform = choice(self.platforms)
                    self.movingTiles.append(DartTrap(platform.x, platform.y, self.tileSize, -20,
                        randint(60, 100) - self.num, self))


    def generateNewStage(self, app):
        print(self.num)
        startY = self.endY
        if (self.num % 15 == 0):
            return HaunterStage(self.width, self.height, self.num + 1)
        elif (self.num % 15 == 14):
            endY = 15
        elif (self.num % 15 == 1 and self.num != 1):
            app.audio.playMusic("stage.mp3", 0.2)
            endY = randint(12, 17)
        else:
            endY = randint(12, 17)
        return Stage(self.width, self.height, startY, endY, self.num + 1)

    def getTiles(self):
        return self.tiles + self.movingTiles

    def getEntities(self):
        if (self.boss != None):
            return [self.boss] + self.entities
        else:
            return self.entities

class Platform (object):
    def __init__(self, x, y, w, tileSize):
        self.tileSize = tileSize
        self.x = x
        self.y = y
        self.row = y // self.tileSize
        self.col = x // self.tileSize
        self.w = w
        self.wCells = w // self.tileSize 
        rng = random()
        if (rng < 0.1):
            self.type = 4
        elif (rng < 0.2):
            self.type = -1
        else:
            self.type = 1

    def __hash__(self):
        return hash(self.x, self.y, self.w)

    def __repr__(self):
        return f"Platform at {self.x}, {self.y}, type = {self.type}"

    def isValid(self, stage):
        if (self.col + self.wCells + 2 > 39):
            return False
        elif (self.row + 3 > 19):
            return False
        for row in range(self.row - 2, self.row + 3):
            for col in range(self.col - 2, self.col + self.wCells + 3):
                if (stage[row][col] != 0):
                    return False
        return True

    def toStage(self, stage):
        if (self.type < 0 and self.w > 200):
            stage.movingTiles.append(MovingPlatform(self.x, self.y, 
                self.x + self.w - 80, self.y, 80, 4, 0))
        for i in range(self.wCells):
            stage.stage[self.row][self.col + i] = self.type 

class HaunterStage(Stage):
    def __init__(self, width, height, num):
        self.width = width
        self.height = height
        self.tileSize = 40
        self.numRows = height // self.tileSize
        self.numCols = width // self.tileSize
        self.startY = 15
        self.num = num
        self.endY = 15
        self.tiles = []
        self.movingTiles = []
        self.entities = []
        self.generateTiles()
        self.boss = Haunter(30 * 40, 3 * 40, self)

    def generateTiles(self):
        for i in range(0, 12):
            self.tiles.append(Square(40 * i, 15 * self.tileSize, self.tileSize))
        for i in range(2, 7):
            self.tiles.append(Square(40 * i, 11 * self.tileSize, self.tileSize))
        for i in range(3, 8):
            self.tiles.append(Square(40 * i, 7 * self.tileSize, self.tileSize))
        for i in range(2, 7):
            self.tiles.append(Square(40 * i, 3 * self.tileSize, self.tileSize))
        
    def addTiles(self):
        for i in range(12, 40):
            self.tiles.append(Square(40 * i, 15 * self.tileSize, self.tileSize))
        




