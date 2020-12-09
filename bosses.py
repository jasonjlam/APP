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
        super().__init__(x, y, 480, 90 + stage.num)
        self.scale = 6
        self.vx = 0
        self.vy = 0
        self.w = 85 * self.scale
        self.h = 70 * self.scale
        self.frameCount = 0
        self.numFrames = 25
        self.moveTimer = 0
        self.ai = {"jumping": 0, "falling": 0, "averageY": 300,
             "still": 0, "moving": 0}
        self.moveChance = [0.2, 0.2, 0.2, 0.2, 0.2]
        self.text = "A wild Haunter appeared!"
        self.updateBoundingBox()
        self.lastMove = ""
        self.currentMove = "initialized"
        self.enrage = False

    def attack(self, app):
        if (self.currentMove == "nightShade"):
            self.nightShade(app)
        elif (self.currentMove == "hex"):
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
        elif (self.currentMove == "faint"):
            self.faint(app)
        elif (self.enrage):
            if (self.moveTimer == 80):
                self.moveTimer = 0
                self.determineMove(app)
        else:
            if (self.moveTimer == 60):
                self.moveTimer = 0
                self.determineMove(app)

    def adjustProbabilities(self, app):
        self.ai["averageY"] = self.ai["averageY"] * 0.8 + 0.2 * app.player.y
        # print(self.ai)
        moveIndexes = {"nightShade": 0, "hex": 1, "swarm": 2, "shadowBall": 3,
            "lick": 4}
        if (self.lastMove != ""):
            index = moveIndexes[self.lastMove]
            adjust = self.moveChance[index] / 4
            self.moveChance[index] = 0
            # print(self.moveChance)
            if (self.ai["averageY"] < 200):
                self.moveChance[3] += 0.1
            if (self.ai["averageY"] > 400 and self.y > 300):
                self.moveChance[1] += 0.1
            if (4 * self.ai["moving"] > self.ai["still"]):
                self.moveChance[2] += 0.1
            else:
                self.moveChance[0] += 0.1
            self.moveChance[4] += 0.1
            self.ai["moving"] = 0
            self.ai["still"] = 0
            for i in range(len(self.moveChance)):
                if (i != index):
                    self.moveChance[i] += adjust
            total = sum(self.moveChance)
            for i in range(len(self.moveChance)):
                self.moveChance[i] /= total

    def determineMove(self, app):
        self.adjustProbabilities(app)
        rng = random()
        # print(rng)
        if (rng < self.moveChance[0]):
            app.audio.playAudio("haunter")
            self.currentMove = "nightShade"
        elif (rng < sum(self.moveChance[0:2])):
            self.currentMove = "hex"
            app.audio.playAudio("haunter")
        elif (rng < sum(self.moveChance[0:3])):
            app.audio.playAudio("gastly")
            self.currentMove = "swarm"
        elif (rng < sum(self.moveChance[0:4])):
            app.audio.playAudio("haunter")
            self.currentMove = "shadowBall"
        elif (rng < sum(self.moveChance)):
            app.audio.playAudio("haunter")
            self.currentMove = "lick"
        self.lastMove = self.currentMove

    def draw(self, app, canvas):
        self.drawHP(app, canvas)
        # print(int(self.frameCount))
        canvas.create_image(self.x, self.y, anchor = "nw", 
                        image = app.sprites["haunter"]
                        [int(self.frameCount)])
        canvas.create_text(15 * 40, 17 * 40, text = self.text,
                font = "System 36")
        canvas.create_text(70, 500, font = "Arial 15 bold",
            text = f"Move timer: {self.moveTimer}")
    
    def drawBoundingBox(self, canvas):
        x0, y0, x1, y1 = self.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, outline = "green")

    def move(self, app):
        if (abs(app.player.vy > 1)):
            self.ai["moving"] += 1
        else:
            self.ai["still"] += 1
        if (self.hp < 1 and self.currentMove != "faint"):
            self.moveTimer = 0
            self.currentMove = "faint"
            app.audio.playAudio("haunter")
        elif (self.currentMove == "initialized" and self.moveTimer == 0):
            app.audio.playMusic("haunter.mp3", 0.08)
        if (self.hp < 40):
            self.enrage = True
        self.updateBoundingBox()
        self.x += self.vx
        self.y += self.vy
        self.attack(app)
        if (self.currentMove != "faint"):
            self.frameCount += 0.5
            self.frameCount %= 25
        # print("self.moveTimer")
        self.moveTimer += 1

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
            if (self.enrage):
                vx = -8
            else:
                vx = -6
            app.stage.entities += [HelixBall(x0, y1, 50, vx, 25, 60)]
            app.stage.entities += [HelixBall(x0, y1, 50, vx, -25, 60)]


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
            self.x = 30 * 40
            self.y = -500
            self.vy = 7
        elif (self.moveTimer % 25 == 22):
            self.vy = 0.5
        elif (self.moveTimer % 25 == 3):
            self.vy = 7
        elif (self.moveTimer > 20 and 
            (self.moveTimer % 25 == 21 or self.moveTimer % 25 == 4)):
            if (self.enrage):
                size = 65
                vx = -25
            else:
                size = 50
                vx = -20
            app.stage.entities += [Ball(x0, y1, size, vx, 0)]

    def exitRight(self, app):
        if (self.moveTimer == 1):
            self.vx = 16
        elif (self.moveTimer > 30):
            self.moveTimer = 0
            self.currentMove = "returnToCenter"

    def returnToCenter(self, app):
        if (self.moveTimer == 1):
            self.x = 40 * 40
            self.vy = 0
            self.vx = -16
            self.y = randint(0, 400)
            if (self.enrage):
                self.text = "The wild Haunter is enraged!"
            else:
                self.text = "The wild Haunter is charging up!"
        elif (self.moveTimer > 26):
            self.x = 30 * 40
            self.vx = 0
            self.moveTimer = 0
            self.currentMove = ""

    def lick(self, app):
        self.text = "The wild Haunter used Lick!"
        if (self.moveTimer == 100):
            self.moveTimer = 0
            self.currentMove = "returnToCenter"
        if (self.moveTimer == 60):
            if (app.player.vy > 0):
                self.ai["jumping"] += 1
            elif (app.player.vy < 0):
                self.ai["falling"] += 1
        elif (self.moveTimer == 30):
            if (self.ai["jumping"] > self.ai["falling"]):
                adjust = -75
            else:
                adjust = 75
            if (self.enrage):
                scale = 25
            else:
                scale = 30
            vectorX = app.player.x - self.x
            vectorY = app.player.y - self.y - 200 + adjust
            self.vx = vectorX / scale
            self.vy = vectorY / scale
        elif (self.moveTimer < 30):
            self.vx = 3
        elif (self.moveTimer < 15):
            self.vx = 0

    def swarm(self, app):
        self.text = "A swarm of Gastlys appeared!"
        if (self.moveTimer == 150):
            self.moveTimer = 0
            self.currentMove = "exitRight"
        if (self.enrage):
            if (self.moveTimer % 13 == 0):
                app.stage.entities += [Gastly(1600, randint(0, 800), app)]
        else:
            if (self.moveTimer % 16 == 0):
                app.stage.entities += [Gastly(1600, randint(0, 800), app)]

        
    def nightShade(self, app):
        self.text = "The wild Haunter used Night Shade!"
        if (self.moveTimer > 90):
            self.moveTimer = 0
            self.currentMove = "exitRight"
        if (self.moveTimer == 10):
            if (self.ai["averageY"] < 200):
                y0 = 0
                y1 = 400
            elif (self.ai["averageY"] > 500):
                y0 = 300
                y1 = 700
            else:
                y0 = int(self.ai["averageY"] - 200)
                y1 = int(self.ai["averageY"] + 200)
            if (self.enrage):
                num = 13
            else:
                num = 10
            for i in range(num):
                app.stage.entities += [Marker(randint(0, 450), randint(y0, y1))]

    def faint(self, app):
        self.text = "The wild Haunter fainted!"
        if (self.moveTimer > 140):
            app.stage.boss = None
            app.stage.addTiles()
        elif (self.moveTimer == 40):
            self.vy = 60
            app.audio.playMusic("victory.mp3", 0.2)
        elif (self.moveTimer < 40):
            self.vx = 0
            self.vy = 0