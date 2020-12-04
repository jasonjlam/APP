from entities import *

class Boss(Entity):
    def __init__(self, x, y, size, hp):
        super().__init__(x,y, size)
        self.hp = hp
        self.maxHP = hp

    def drawHP(self, app, canvas):
        hp = self.hp / self.maxHP
        canvas.create_rectangle(0, 0, app.stage.width, 10, fill = "red")
        canvas.create_rectangle(0, 0, hp * app.stage.width, 10, fill = "green")

class Haunter(Boss):
    def __init__(self, x, y):
        super().__init__(x, y, 480, 150)
        self.scale = 6
        self.w = 85 * self.scale
        self.h = 70 * self.scale
        self.frameCount = 0
        self.numFrames = 25
        self.moveTimer = 0
        self.text = "A wild Haunter appeared!"
        self.updateBoundingBox()

    def draw(self, app, canvas):
        print(self.hp)
        self.drawHP(app, canvas)
        # print(int(self.frameCount))
        canvas.create_image(self.x, self.y, anchor = "nw", 
                        image = app.sprites["haunter"]
                        [int(self.frameCount)])
        canvas.create_rectangle(self.boundingBox)
        canvas.create_text(15 * 40, 17 * 40, text = self.text,
                font = "System 36")

    def move(self, app):
        if (self.hp < 1):
            app.stage.boss = None
        self.updateBoundingBox()
        x0, y0, x1, y1 = self.boundingBox
        self.frameCount += 0.5
        self.frameCount %= 25
        self.moveTimer += 1
        print(self.moveTimer)
        if (self.moveTimer == 120):
            self.moveTimer = 0
            app.stage.entities += [HelixBall(x0, y0, 50, -6, 20, 60)]
            app.stage.entities += [HelixBall(x0, y0, 50, -6, -20, 60)]
        pass

    def updateBoundingBox(self):
        if (self.frameCount < 14):
            offset = 0.6 * (13 - self.frameCount)
        elif (self.frameCount > 16):
            offset = 0.9 * abs(17 - self.frameCount)
        else:
            offset = -3
        x0 = self.x + 22 * self.scale
        y0 = self.y + (19 - offset) * self.scale
        x1 = x0 + 34 * self.scale
        y1 = y0 + 30 * self.scale
        self.boundingBox = (x0, y0, x1, y1)

    def isTouching(self, boundingBoxes):
        for box in boundingBoxes:
            boundingBox = boundingBoxes[box]
            if (boxesIntersect(boundingBox, self.boundingBox)):
                return True
        return False

    def isProjectileTouching(self, x, y, r):
        return boxIntersectsCircle(self.boundingBox, x, y, r)

