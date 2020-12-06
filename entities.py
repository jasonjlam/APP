# Contains all of the hostile entities, that subclass the Entity class
# Entity class is subclassed from Tile for center and proximity methods

from tiles import *
from math import *
from random import *

class Entity(Tile):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.hp = -100
        self.moving = False

    def move(self, app, yOffset = 300):
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
        if (self.isTouching(app.player.boundingBoxes)):
            self.color = "red"
        elif (self.color == "red"):
            self.color = "purple"
            
    def drawBoundingBox(self):
        pass

    def draw(self):
        pass

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
        canvas.create_line(x + size / 2, y, x, y + size)
        canvas.create_line(x + size / 2, y, x + size, y + size)
        canvas.create_line(x, y + size, x + size, y + size)

    def drawBoundingBox(self, canvas):
        for box in self.boundingBoxes:
            x0, y0, x1, y1 = box
            canvas.create_rectangle(x0, y0, x1, y1, outline = "green")

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
    
    def isProjectileTouching(self, x, y, r):
        return (((self.x - x) ** 2 + (self.y - y) ** 2) <= (r + self.r) ** 2)

    def drawBoundingBox(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r,
            self.y + self.r, outline = "green")

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

class Gastly(Ball):
    def __init__(self, x, y, app):
        super().__init__(x, y, 26, 0, 0)
        self.hp = 1
        self.initialMove(app)
        self.display = True
        self.homing = False
        self.timer = 0

    def initialMove(self, app):
        vectorX = app.player.x - self.x - randint(-100, 100)
        vectorY = app.player.y - self.y - randint(-100, 100) 
        vectorLength = int((vectorX **2 + vectorY **2)** 0.5)
        self.vx = vectorX / vectorLength * 10
        self.vy = vectorY / vectorLength * 10

    def move(self, app):
        if (not self.display):
            app.stage.entities.remove(self)
        elif (self.hp == 0 or self.timer > 500):
            self.display = False
        vectorX = app.player.x - self.x 
        vectorY = app.player.y - self.y
        distance = vectorX ** 2 + vectorY ** 2
        if (self.homing and distance > 20000):
            if (self.vx < -6):
                self.vx += 1
            elif (self.vx > 6):
                self.vx -= 1
            elif (vectorX - self.vx > 0):
                self.vx += 1
            else:
                self.vx -= 1
            if (self.vy < -6):
                self.vy += 1
            elif (self.vy > 6):
                self.vy -= 1
            elif (vectorY - self.vy > 0):
                self.vy += 1
            else:
                self.vy -= 1
        elif (distance < 40000):
            self.homing = True
            self.color = "blue"

        self.timer += 1
        super().move(app, 500)

    def draw(self, app, canvas):
        x = self.x - 58
        y = self.y - 56
        canvas.create_image(x, y, anchor = "nw", image = app.sprites["gastly"])

class Marker(Ball):
    def __init__(self, x, y):
        super().__init__(x, y, 8, 0, 0)
        self.timer = 0
        self.moving = True

    def move(self, app):
        if (self.timer > 30):
            size = 125
            app.stage.entities += [NightShade(self.x - size / 2,
                self. y - size / 2, size)]
            app.stage.entities.remove(self)
        self.timer += 1

    def draw(self, app, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r,
            self.y + self.r, fill = "red")

    def isTouching(self, boundingBoxes):
        return False

class NightShade(Entity):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.timer = 0
        self.moving = True
        self.boundingBox = (x, y, x + size, y + size)
    
    def move(self, app):
        if (self.timer > 100):
            app.stage.entities.remove(self)
        self.timer += 1

    def drawBoundingBox(self, canvas):
        x0, y0, x1, y1 = self.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, outline = "green")

    def draw(self, app, canvas):
        x = self.x
        y = self.y
        size = self.size
        canvas.create_rectangle(x, y, x + size, y + size, fill = "purple")

    def isTouching(self, boundingBoxes):
        for box in boundingBoxes:
            boundingBox = boundingBoxes[box]
            if (boxesIntersect(self.boundingBox, boundingBox)):
                return True
        return False

