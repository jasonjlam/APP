# Holds all of the tiles for each stage, and their many different types

from cmu_112_graphics import *
from entities import *

class Tile(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = "black"

    def __repr__(self):
        return f"{type(self)} at ({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.x, self.y, self.size)

    def centerOfTile(self):
        return (self.x, self.y)
    
    def inProximity(self, x, y, extra = 25):
        d = self.size + extra
        cx, cy = self.centerOfTile()
        return abs(cx - x) < d and abs(cy - y) < d

    def draw(self, app, canvas):
        pass

class Square(Tile):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.boundingBox = (x, y, x + size, y + size)
        self.size = size

    def centerOfTile(self):
        return (self.x + self.size / 2, self.y + self.size / 2)

    def draw(self, app, canvas):
        x0, y0, x1, y1 = self.boundingBox
        canvas.create_image(x0, y0, image = app.sprites["dirt"], anchor = "nw")


class MovingPlatform(Tile):
    def __init__(self, x0, y0, x1, y1, size, vx, vy):
        super().__init__(x0 + vx, y0 + vy, size)
        self.thickness = 10
        self.boundingBox = (x0, y0, x0 + size, y0 + self.thickness)
        self.oldBoundingBox = self.boundingBox
        self.vx = vx
        self.vy = vy 
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def centerOfTile(self):
        return (self.x + self.size / 2, self.y + self.thickness / 2)

    def move(self):
        self.oldBoundingBox = self.boundingBox
        self.lastx = self.x
        self.lasty = self.y
        self.x += self.vx
        self.y += self.vy
        if ((self.x == self.x1 or self.x == self.x0) and self.vx != 0 ):
            self.vx = -self.vx
        if ((self.y == self.y1 or self.y == self.y0) and self.vy != 0 ):
            self.vy = -self.vy
        self.boundingBox = (self.x, self.y, self.x + self.size, 
                            self.y + self.thickness)

    def onPlatform(self, boundingBoxes):
        x0, y0, x1, y1 = boundingBoxes["left"]
        x2, y2, x3, y3 = boundingBoxes["right"]
        x4, y4, x5, y6 = self.boundingBox
        return (x3 > x4 and x0 < x5)

class Save(Square):
    def __init__(self, x, y, size, stage):
        super().__init__(x,y, size)
        self.stage = stage
        self.color = "red"

class VanishingTile(Square):
    def __init__(self, x, y, size, stage):
        super().__init__(x,y, size)
        self.timer = 0
        self.stage = stage

    def move(self):
        if (self.timer > 20):
            self.stage.movingTiles.remove(self)
        elif (self.timer > 0):
            self.timer += 1

class FireBar(Square):
    def __init__(self, x, y, size, r, period, direction, stage):
        super().__init__(x, y, size)
        self.period = period
        self.r = r
        self.stage = stage
        self.ballR = 10
        self.direction = direction
        self.createFireballs(stage)

    def createFireballs(self, stage):
        self.fireballs = []
        r = 0
        cx, cy = self.centerOfTile()
        while (self.r > r):
            newCX = cx + r
            stage.entities += [RotatingBall(newCX, cy, self.ballR, r, 
                self.direction, self.period)]
            r += self.ballR * 2



