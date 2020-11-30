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
        self.onPlatform = None
        self.isJumping = False
        self.jumps = 2
        self.updateBoundingBoxes(0,0)
        self.doubleJumpPrimed = False

    def jump(self, app):
        # print(self.doubleJumpPrimed)
        if (self.jumps > 1 and self.vy > -3 or 
            (self.jumps > 0  and self.vy > -3 and self.doubleJumpPrimed)):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.onPlatform = None
            self.onGround = False
            self.jumps -= 1


    def setvx(self, vx):
        self.vx = vx

    def move(self, stage):
        start = time.time()
        # print (self.vx, self.vy)
        # print(self.onGround)
        # print(self.doubleJump)
        print (self.onPlatform)
        if (self.vy < 0):
            self.onGround = False
        self.moveJump()
        tiles = []
        for tile in stage.getTiles():
            if (tile.inProximity(self.x + 25, self.y + 25, 80)):
                tiles += [tile]
        self.moveWithCollision(stage, self.vx, self.vy, tiles)
        # print(self.x, self.y)
        self.updateBoundingBoxes(self.x, self.y)
        # print (time.time() - start)
    
    def moveWithCollision(self, stage, vx, vy, tiles, depth = 0):
        print("Start", vx)
        if (vx == 0 and vy == 0):
            return (0, 0)
        vLength = int(vx ** 2 + vy ** 2) + 1
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
                    if (collisions["left"] or collisions["right"]):
                        self.vx = 0
                        if (collisions["vx"] != 0):
                            currentVX += collisions["vx"]
                            self.vx = collisions["vx"]
                        self.x += currentVX
                        self.moveWithCollision(stage, 0, vy, tiles, 1)
                        return
                    if (collisions["top"] or collisions["bot"]):
                        self.vy = 0
                        if (collisions["vy"] != 0):
                            if (self.isJumping):
                                currentVY += -30
                                self.onPlatform = False
                            else:
                                currentVY += collisions["vy"]
                            self.vy = collisions["vy"]
                            print(currentVX, self.vx, currentVY, self.vy)
                        vy = currentVY
                        self.x += vx
                        self.y += vy
                        return 
        self.vx = vx
        self.vy = vy
        self.x += vx
        self.y += vy

    def checkCollisions(self, stage, vx, vy, tiles, depth):
        # print("Collisions being checked")
        # print(tiles)
        collisions = {"top": False, "left": False, "right": False, "bot": False,
        "vx": 0, "vy": 0, "platform": False}
        self.updateBoundingBoxes(self.x + vx, self.y + vy)
        boundingBox = self.boundingBoxes
        for tile in tiles:
            if (isinstance(tile, MovingPlatform)):
                debug = True
            else:
                debug = False
            if (vy >= 0 or debug):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["bot"], debug)):
                    collisions["bot"] = True
                    print("bot")
                    if (isinstance(tile, MovingPlatform)):
                        collisions["platform"] = True
                        self.onPlatform = True
                        collisions["vy"] = tile.vy
            if (vy <= 0):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["top"])):
                    collisions["top"] = True
            if (vx <= 0 and depth < 1 and not self.onPlatform):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["left"])):
                    collisions["left"] = True
                    # if (isinstance(tile, MovingPlatform)):
                    #     vx = tile.vx
                    #     collisions["vx"] = tile.vx
            elif (vx >= 0 and depth < 1 and not self.onPlatform):
                if (tile.boxesIntersect(tile.boundingBox, 
                                        boundingBox["right"])):
                    collisions["right"] = True
                    # if (isinstance(tile, MovingPlatform)):
                    #     vx = tile.vx
                    #     collisions["vx"] = tile.vx
        if (collisions["bot"] or collisions["platform"]):
            self.onGround = True
            self.jumps = 2
            self.doubleJumpPrimed = False
        else:
            self.onGround = False
            self.onPlatform = False
        return collisions

    def updateBoundingBoxes(self, x, y):
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

