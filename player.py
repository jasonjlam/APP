# The player class, which handles all collisions and movement

import time
from tiles import *

class Player(object):
    def __init__(self, x, y):
        # print("Creating player")
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 48
        self.h = 44
        self.jumpVelocity = -24
        self.onGround = True
        self.onPlatform = False
        self.isJumping = False
        self.platformVX = 0
        self.platformVY = 0
        self.jumps = 2
        self.updateBoundingBoxes(0,0)
        self.doubleJumpPrimed = False

    def jump(self, app):
        # print(self.doubleJumpPrimed)
        if (self.jumps > 1 and self.vy > -3 or 
            (self.jumps > 0  and self.vy > -3 and self.doubleJumpPrimed)):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.onPlatform = False
            self.onGround = False
            self.jumps -= 1


    def setvx(self, vx):
        self.vx = vx

    def move(self, stage):
        start = time.time()
        # print (self.vx, self.vy)
        # print(self.onGround)
        # print(self.doubleJump)
        # print (self.onPlatform)
        if (self.vy < 0):
            self.onGround = False
        self.moveJump()
        tiles = []
        for tile in stage.getTiles():
            if (tile.inProximity(self.x + 25, self.y + 25)):
                tiles += [tile]
        platform = self.groundCheck(stage, tiles)
        print(self.x, self.y)
        self.moveWithCollision(stage, self.vx, self.vy, tiles, platform)
        print(self.x, self.y)
        self.updateBoundingBoxes(self.x, self.y)
        # print (time.time() - start)
        return self.checkBorders(stage)
    
    def groundCheck(self, stage, tiles):
        print(self.onPlatform)
        ground = False
        platform = False
        x0, y0, x1, y1 = self.boundingBoxes["bot"]
        box = (x0, y0, x1, y1 + 1)
        for tile in tiles:
            if (tile.boxesIntersect(box, tile.boundingBox, "true")):
                touching = True
                if (isinstance(tile, MovingPlatform)):
                    print("AHHH")
                    platform = True
                    self.x += tile.getLastVX()
                    if (tile.getLastVY() < 0):
                        self.y += tile.getLastVY()
                    # self.updateGround(ground, platform)
                    # return (vx, vy)
        print(ground, platform)
        self.updateGround(ground, platform)
        


    def moveWithCollision(self, stage, vx, vy, tiles, platform, depth = 0):
        # print("Start", vx)
        if (vx == 0 and vy == 0):
            return (0, 0)
        vLength = int(vx ** 2 + vy ** 2) // 2 + 1
        xStep = vx / vLength
        yStep = vy / vLength
        currentVX = 0
        currentVY = 0
        currentStep = 0
        while (currentStep < vLength):
            currentStep += 1
            currentVX += xStep
            currentVY += yStep
            collisions = self.checkCollisions(stage, currentVX, 
                                        currentVY, tiles, depth)
            for key in collisions:
                if (collisions[key]):
                    currentVX -= xStep
                    currentVY -= yStep
                    if ((collisions["left"] or collisions["right"]) 
                                            and vx != 0):
                        self.vx = 0
                        # if (collisions["vx"] != 0):
                        #     currentVX += collisions["vx"]
                        #     self.vx = collisions["vx"]
                        print("currentVX", currentVX)
                        self.x += currentVX
                        if (depth < 1):
                            self.moveWithCollision(stage, 0, vy, tiles, 1)
                        else:
                            print("Case 1")
                            self.y += currentVY
                        return
                    if ((collisions["top"] or collisions["bot"]) and vy != 0):
                        self.vy = 0
                        print("currentVY", currentVY)
                        self.y += currentVY
                        if (depth < 1):
                            self.moveWithCollision(stage, vx, 0, tiles, 1)
                        else:
                            print("Case 2")
                            self.x += currentVX
                        return 
        self.vx = vx
        self.vy = vy
        self.x += vx
        self.y += vy

    def checkCollisions(self, stage, vx, vy, tiles, depth):
        # print("Collisions being checked")
        # print(tiles)
        collisions = {"top": False, "left": False, "right": False, "bot": False,
         "platform": False, "vx": 0, "vy": 0}
        self.updateBoundingBoxes(self.x + vx, self.y + vy)
        boundingBox = self.boundingBoxes
        for tile in tiles:
            if (vy >= 0):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["bot"])):
                    collisions["bot"] = True
                    if (isinstance(tile, MovingPlatform)):
                        collisions["platform"] = True
                        collisions["vx"] = tile.getLastVX()
                        collisions["vy"] = tile.getLastVY()
                    print("bot")
            if (vy <= 0):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["top"])):
                    collisions["top"] = True
            if (vx <= 0):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["left"])):
                    collisions["left"] = True
            elif (vx >= 0):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["right"])):
                    print("Right intersection")
                    collisions["right"] = True
        self.updateGround(collisions["bot"], collisions["platform"])
        return collisions

    def updateGround(self, isTouching, isPlatform):
        if (isTouching):
            if (isPlatform):
                self.onPlatform = True
            else:
                self.onGround = True
            self.jumps = 2
            self.doubleJumpPrimed = False
        else:
            self.onGround = False
            self.onPlatform = False

    def updateBoundingBoxes(self, x, y):
        x = round(x)
        y = round(y)
        self.boundingBoxes = {"top": (1 + x, 0 + y, 46 + x, 1 + y), 
        "left": (0 + x, 2 + y, 24 + x, 40 + y), 
        "right": (25 + x, 2 + y, 47 + x, 40 + y),
        "bot": (1 + x, 20 + y, 46 + x, 42 + y)}

    def moveJump(self):
        if (self.vy < -9 and not self.isJumping):
            self.vy = -9
            self.onGround = False
        if (not self.onGround and not self.onPlatform):
            self.vy += 3
        if (self.vy > 25):
            self.vy = 25

    def checkBorders(self, stage):
        border = None
        if (self.x < -25):
            border = "left"
            self.x = stage.width - 23
        elif (self.x > stage.width - 25):
            border = "right"
            self.x = -23
        elif (self.y < -25):
            border = "top"
            self.y = stage.height - 23
            self.vy += -10
        elif (self.y > stage.height + 25):
            border = "bot"
            self.y = -23
        # print(border, stage.entrance, stage.exit)
        if (border == stage.exit):
            return 1
        elif (border == stage.entrance):
            return -1
        else:
            return 0



