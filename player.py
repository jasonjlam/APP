import time

class Player(object):
    def __init__(self, x, y):
        # print("Creating player")
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 48
        self.h = 44
        self.jumpVelocity = -30
        self.onGround = True
        self.isJumping = False
        self.jumps = 2
        self.radius = 50
        self.updateBoundingBoxes(0,0)
        self.doubleJumpPrimed = False

    def jump(self, app):
        # print(self.doubleJumpPrimed)
        if (self.jumps > 1 and self.vy > -3 or 
            (self.jumps > 0  and self.vy > -3 and self.doubleJumpPrimed)):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.onGround = False
            self.jumps -= 1


    def setvx(self, vx):
        self.vx = vx

    def move(self, stage):
        start = time.time()
        # print (self.vx, self.vy)
        # print(self.onGround)
        # print(self.doubleJump)
        if (self.vy < 0):
            self.onGround = False
        self.moveJump()
        tiles = []
        for tile in stage.tiles:
            if (tile.inProximity(self.x + 25, self.y + 25, 70)):
                tiles += [tile]
        x, y = self.moveWithCollision(stage, self.vx, self.vy, tiles)
        self.x += x
        self.y += y
        self.updateBoundingBoxes(self.x, self.y)
        # print (time.time() - start)
    
    def moveWithCollision(self, stage, vx, vy, tiles):
        print(tiles)
        if (vx == 0 and vy == 0):
            return (0, 0)
        vLength = int((vx ** 2 + vy ** 2) ** 0.5) * 2
        xStep = vx / vLength
        yStep = vy / vLength
        currentVX = 0
        currentVY = 0
        i = 0
        currentStep = 0
        while (currentStep < vLength):
            currentStep += 1
            currentVX += xStep
            currentVY += yStep
            collisions = self.checkCollisions(stage, currentVX, 
                                        currentVY, tiles)
            for key in collisions:
                if (collisions[key]):
                    currentVX -= xStep
                    currentVY -= yStep
                    if (collisions["left"] or collisions["right"]):
                        vx = currentVX
                        self.vx = 0
                    if (collisions["top"] or collisions["bot"]):
                        vy = currentVY
                        self.vy = 0
                    return (vx, vy)
        self.vx = vx
        self.vy = vy
        return (vx, vy)

    def checkCollisions(self, stage, vx, vy, tiles):
        # print("Collisions being checked")
        # print(tiles)
        collisions = {"top": False, "left": False, "right": False, "bot": False}
        self.updateBoundingBoxes(self.x + vx, self.y + vy)
        boundingBox = self.boundingBoxes
        for tile in tiles:
                if (vy <= 0):
                    if (tile.boxesIntersect(boundingBox["top"])):
                        collisions["top"] = True
                elif (vy >= 0):
                    if (tile.boxesIntersect(boundingBox["bot"])):
                        collisions["bot"] = True
                if (vx <= 0):
                    if (tile.boxesIntersect(boundingBox["left"])):
                        collisions["left"] = True
                elif (vx >= 0):
                    if (tile.boxesIntersect(boundingBox["right"])):
                        collisions["right"] = True
        if (collisions["bot"]):
            self.onGround = True
            self.jumps = 2
            self.doubleJumpPrimed = False
        else:
            self.onGround = False
        return collisions

    def updateBoundingBoxes(self, x, y):
        self.boundingBoxes = {"top": (1 + x, 0 + y, 46 + x, 1 + y), 
        "left": (0 + x, 2 + y, 24 + x, 40 + y), 
        "right": (25 + x, 2 + y, 47 + x, 40 + y),
        "bot": (1 + x, 41 + y, 46 + x, 42 + y)}

    def moveJump(self):
        if (self.vy < -9 and not self.isJumping):
            self.vy = -9
            self.onGround = False
        if (not self.onGround):
            self.vy += 2.5
        if (self.vy > 20):
            self.vy = 20

