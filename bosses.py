from entities import *
from random import *

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
    def __init__(self, x, y, stage):
        super().__init__(x, y, 480, 120)
        self.stage = stage
        self.scale = 6
        self.vx = 0
        self.vy = 0
        self.w = 85 * self.scale
        self.h = 70 * self.scale
        self.frameCount = 0
        self.numFrames = 25
        self.moveTimer = 0
        self.text = "A wild Haunter appeared!"
        self.updateBoundingBox()
        self.currentMove = ""

    def draw(self, app, canvas):
        self.drawHP(app, canvas)
        # print(int(self.frameCount))
        canvas.create_image(self.x, self.y, anchor = "nw", 
                        image = app.sprites["haunter"]
                        [int(self.frameCount)])
        canvas.create_text(15 * 40, 17 * 40, text = self.text,
                font = "System 36")
    
    def drawBoundingBox(self, canvas):
        x0, y0, x1, y1 = self.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, outline = "green")

    def move(self, app):
        if (self.hp < 1):
            app.stage.boss = None
            self.text = "The wild Haunter fainted!"
        self.updateBoundingBox()
        self.x += self.vx
        self.y += self.vy
        print(self.x, self.y)
        if (self.currentMove == "hex"):
            self.hex(app)
        elif (self.currentMove == "swarm"):
            self.swarm(app)
        elif (self.currentMove == "shadowBall"):
            self.shadowBall(app)
        elif (self.currentMove == "lick"):
            self.lick(app)
        elif (self.currentMove == "exitRight"):
            self.exitRight(app)
        elif (self.currentMove == "returnToCenter"):
            self.returnToCenter(app)
        elif (self.moveTimer == 100):
            self.moveTimer = 0
            self.currentMove = "swarm"
        self.frameCount += 0.5
        self.frameCount %= 25
        self.moveTimer += 1
        print(self.moveTimer)

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

    def hex(self, app):
        self.text = "The wild Haunter used Hex!"
        x0, y0, x1, y1 = self.boundingBox
        if (self.moveTimer > 20):
            self.moveTimer = 0
            self.currentMove = "exitRight"
        elif (self.moveTimer == 1):
            app.stage.entities += [HelixBall(x0, y1, 50, -6, 20, 60)]
            app.stage.entities += [HelixBall(x0, y1, 50, -6, -20, 60)]


    def shadowBall(self, app):
        self.text = "The wild Haunter used Shadow Ball!"
        x0, y0, x1, y1 = self.boundingBox
        if(self.moveTimer == 215):
            self.moveTimer = 0
            self.currentMove = "returnToCenter"
        elif (self.moveTimer >= 180):
            self.vy = 15
        elif (self.moveTimer == 1):
            self.vx = 20
        elif (self.moveTimer == 15):
            self.vx = 0
            self.x = 20 * 40
            self.y = -500
            self.vy = 7
        elif (self.moveTimer % 25 == 22):
            self.vy = 0.5
        elif (self.moveTimer % 25 == 3):
            self.vy = 7
        elif (self.moveTimer > 20 and 
            (self.moveTimer % 25 == 21 or self.moveTimer % 25 == 4)):
            app.stage.entities += [Ball(x0, y1, 50, -20, 0)]

    def exitRight(self, app):
        if (self.moveTimer == 1):
            self.vx = 16
        elif (self.moveTimer > 30):
            self.moveTimer = 0
            self.currentMove = "returnToCenter"

    def returnToCenter(self, app):
        if (self.moveTimer == 1):
            self.x = 30 * 40
            self.vy = 0
            self.vx = -16
            self.y = randint(0, 400)
        elif (self.moveTimer > 26):
            self.x = 20 * 40
            self.vx = 0
            self.moveTimer = 0
            self.currentMove = ""

    def lick(self, app):
        self.text = "The wild Gastly used Lick!"
        if (self.moveTimer == 100):
            self.moveTimer = 0
            self.currentMove = "returnToCenter"
        elif (self.moveTimer == 30):
            vectorX = app.player.x - self.x
            vectorY = app.player.y - self.y - 200
            self.vx = vectorX / 30
            self.vy = vectorY / 30
        elif (self.moveTimer < 30):
            self.vx = 3
        elif (self.moveTimer < 15):
            self.vx = 0

    def swarm(self, app):
        self.text = "A swarm of Gastlys appeared!"
        if (self.moveTimer == 150):
            self.moveTimer = 0
            self.currentMove = "exitRight"
        elif (self.moveTimer % 16 == 0):
            app.stage.entities += [Gastly(1200, randint(0, 800), app)]

        
    # def meanLook(self, app):