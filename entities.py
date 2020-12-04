# Contains all of the hostile entities, that subclass the Entity class
# Entity class is subclassed from Tile for center and proximity methods

from tiles import *
from math import *

class Entity(Tile):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.hp = -100
        self.moving = False

    def move(self, app, yOffset):
        entities = app.stage.entities
        self.x += self.vx
        self.y += self.vy
        x = self.x
        y = self.y
        if (self.x < 0 - self.size / 2 or self.x > app.stage.width + 
            self.size / 2 or self.y < 0 - yOffset or
            self.y > app.stage.height + yOffset):
            entities.remove(self)
            return
        if self.isTouching(app.player.boundingBoxes):
            print("touching")
            self.color = "red"
        else:
            self.color = "purple"

class UpwardSpike(Entity):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.boundingBoxes = self.createBoundingBoxes()

    def createBoundingBoxes(self):
        boxes = []
        x = self.x + self.size / 2
        y = self.y
        size = self.size
        index = 1
        while(y < self.y + size):
            boxes.append((x - size / 8 * index, y, x + size / 8 * index, 
                            y + size / 4))
            y += size / 4   
            index += 1
        return boxes

    def centerOfTile(self):
        return (self.x + self.size / 2, self.y + self.size / 2)

    def isTouching(self, boundingBoxes):
        playerBox = boundingBoxes["bot"]
        for spikeBox in self.boundingBoxes:
            if (boxesIntersect(spikeBox, playerBox)):
                return True
        return False

    def draw(self, app, canvas):
        x = self.x
        y = self.y
        size = self.size
        for box in self.boundingBoxes:
            x0, y0, x1, y1 = box
            canvas.create_rectangle(x0, y0, x1, y1)
        canvas.create_line(x + size / 2, y, x, y + size)
        canvas.create_line(x + size / 2, y, x + size, y + size)
        canvas.create_line(x, y + size, x + size, y + size)

class Ball(Entity):
    def __init__(self, x, y, size, vx, vy):
        self.x = x
        self.y = y
        self.size = size * 2
        self.r = size
        self.vx = vx
        self.vy = vy
        self.hp = -100
        self.moving = True
        self.color = "purple"

    def __hash__(self):
        return hash(self.x, self.y, self.vx)

    def __repr__(self):
        return f"Projectile at ({self.x}, {self.y}), velocity = "
        + f"{self.vx, self.vy}"

    def isTouching(self, boundingBoxes):
        for box in boundingBoxes:
            boundingBox = boundingBoxes[box]
            if (boxIntersectsCircle(boundingBox, self.x, self.y, self.r)):
                return True
        return False

    def draw(self, app, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r,
            self.y + self.r, fill = self.color)

class HelixBall(Ball):
    def __init__(self, x, y, size, vx, vy, period):
        super().__init__(x, y, size, vx, vy)
        self.maxVY = vy
        self.theta = 0
        self.period = 60


    def move(self, app):
        self.theta += 1
        if (self.theta >= self.period):
            self.theta = 0
        self.vy = self.maxVY * cos(self.theta * 2 * pi / self.period)
        super().move(app, 500)
