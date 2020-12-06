# Holds all of the tiles for each stage, and their many different types

from cmu_112_graphics import *

def boxesIntersect(box1, box2, debug = False):
    if (debug):
        print(box1, box2)
    x0, y0, x1, y1 = box1
    x2, y2, x3, y3 = box2
    offset = 0.1
    return not (x2 - offset >= x1 or x0 - offset >= x3 
            or y2 - offset >= y1 or y0 - offset >= y3)

def isPointIn(box, x, y):
    x0, y0, x1, y1 = box
    return (x > x0 and x < x1 and y > y0 and y < y1)

def boxIntersectsCircle(box, x, y, r):
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    xDistance = abs((x0 + x1) / 2 - x)
    yDistance = abs((y0 + y1) / 2 - y)

    if (xDistance > w / 2 + r or yDistance > h / 2 + r):
        return False
    elif (xDistance <= w / 2 or yDistance <= h / 2):
        return True
    return ((xDistance - w / 2)**2 + (yDistance - h / 2) **2 <= r ** 2)

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

class Square(Tile):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.boundingBox = (x, y, x + size, y + size)
        self.size = size

    def centerOfTile(self):
        return (self.x + self.size / 2, self.y + self.size / 2)


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



