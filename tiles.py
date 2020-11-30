# Holds all of the tiles for each stage, and their many different types

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

    def boxesIntersect(self, box1, box2, debug = False):
        # if (debug):
            # print(box1, box2)
        x0, y0, x1, y1 = box1
        x2, y2, x3, y3 = box2
        return not (x2 >= x1 or x0 >= x3 or y2 >= y1 or y0 >= y3)

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
        self.vx = vx
        self.vy = vy 
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if ((self.x == self.x1 or self.x == self.x0) and self.vx != 0 ):
            self.vx = -self.vx
        if ((self.y == self.y1 or self.y == self.y0) and self.vy != 0 ):
            self.vy = -self.vy
        self.boundingBox = (self.x, self.y, self.x + self.size, 
                            self.y + self.thickness)

