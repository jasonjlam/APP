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
        self.platform = None
        self.isJumping = False
        self.jumps = 2
        self.updateBoundingBoxes(0,0)
        self.doubleJumpPrimed = False
        self.facing = 1
        self.projectiles = []
        self.death = False

    def shoot(self):
        if (len(self.projectiles) < 5):
            offset = 25
            self.projectiles += [PlayerProjectile(self.x + offset + 
                self.facing * offset, self.y + 15, self.facing * 16)]

    def jump(self, app):
        # print(self.doubleJumpPrimed)
        if (self.jumps > 1 and self.vy > -3 or 
            (self.jumps > 0  and self.vy > -3 and self.doubleJumpPrimed)):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.platform = None
            self.onGround = False
            self.jumps -= 1

    def moveJump(self):
        if (self.vy < -9 and not self.isJumping):
            self.vy = -9
            self.onGround = False
        if (not self.onGround and self.platform == None):
            self.vy += 3
        if (self.vy > 25):
            self.vy = 25

    def move(self, stage):
        if (self.vy < 0):
            self.onGround = False
        self.moveJump()
        tiles = []
        for tile in stage.getTiles():
            if (tile.inProximity(self.x + 25, self.y + 25)):
                tiles += [tile]
        entities = []
        for entity in stage.entities:
            if (entity.inProximity(self.x + 25, self.y + 25)):
                entities += [entity]
        self.groundCheck(stage, tiles)
        # print(self.x, self.y)
        self.moveWithCollision(stage, self.vx, self.vy, tiles, entities)
        self.updateBoundingBoxes(self.x, self.y)
        if (self.platform != None):
            if (not self.platform.onPlatform(self.boundingBoxes)):
                self.platform = None
        return self.checkBorders(stage)
    
    def groundCheck(self, stage, tiles):
        ground = False
        platform = False
        x0, y0, x1, y1 = self.boundingBoxes["bot"]
        box = (x0, y0, x1, y1)
        if (self.platform != None):
            self.y = self.platform.y - 42
            self.x += self.platform.vx
        for tile in tiles:
            if (boxesIntersect(box, tile.boundingBox)):
                touching = True
                    # self.updateGround(ground, platform)
                    # return (vx, vy)
        self.updateGround(ground)
        


    def moveWithCollision(self, stage, vx, vy, tiles, entities, depth = 0):
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
                                        currentVY, tiles, entities)
            for key in collisions:
                if (collisions[key]):
                    currentVX -= xStep
                    currentVY -= yStep
                    if ((collisions["left"] or collisions["right"]) 
                                            and vx != 0):
                        self.vx = 0
                        self.x += currentVX
                        if (depth < 1):
                            self.moveWithCollision(stage, 0, vy, tiles, 
                                entities, 1)
                        else:
                            self.y += currentVY
                        return
                    if ((collisions["top"] or collisions["bot"]) and vy != 0):
                        self.vy = 0
                        self.y += currentVY
                        if (depth < 1):
                            self.moveWithCollision(stage, vx, 0, tiles,
                                entities, 1)
                        else:
                            self.x += currentVX
                        return 
        self.vx = vx
        self.vy = vy
        self.x += vx
        self.y += vy

    def checkCollisions(self, stage, vx, vy, tiles, entities):
        # print("Collisions being checked")
        # print(tiles)
        collisions = {"top": False, "left": False, "right": False, "bot": False,
         "platform": False}
        self.updateBoundingBoxes(self.x + vx, self.y + vy)
        boundingBox = self.boundingBoxes
        for entity in entities:
            if (entity.isTouching(boundingBox)):
                self.death = True
        for tile in tiles:
            if (vy >= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["bot"])):
                    collisions["bot"] = True
                    if (isinstance(tile, MovingPlatform)):
                        self.platform = tile
            if (vy <= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["top"])):
                    collisions["top"] = True
            if (vx <= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["left"])):
                    collisions["left"] = True
            elif (vx >= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["right"])):
                    collisions["right"] = True
        self.updateGround(collisions["bot"])
        return collisions

    def updateGround(self, isTouching):
        if (isTouching):
            if (self.platform == None):
                self.onGround = True
            self.jumps = 2
            self.doubleJumpPrimed = False
        else:
            self.onGround = False

    def updateBoundingBoxes(self, x, y):
        x = round(x)
        y = round(y)
        self.boundingBoxes = {"top": (1 + x, 0 + y, 46 + x, 1 + y), 
        "left": (0 + x, 2 + y, 24 + x, 40 + y), 
        "right": (25 + x, 2 + y, 47 + x, 40 + y),
        "bot": (1 + x, 20 + y, 46 + x, 42 + y)}

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
        if (border == stage.exit):
            self.projectiles = []
            return 1
        elif (border == stage.entrance):
            self.projectiles = []
            return -1
        else:
            return 0

class PlayerProjectile(object):
    def __init__(self, x, y, vx):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        r = self.r * 3 / 4
        self.boundingBox = (x - r, y - r, x + r, y - r)

    def __hash__(self):
        return hash(self.x, self.y, self.vy)

    def __repr__(self):
        return f"Projectile at ({self.x}, {self.y}), velocity = {self.vx}"

    def move(self, app):
        projectiles = app.player.projectiles
        stage = app.stage
        self.x += self.vx
        x = self.x
        y = self.y
        r = 3 * self.r / 4
        self.boundingBox = (x - r, y - r, x + r, y + r)
        if (self.x < 0 or self.x > stage.width):
            projectiles.remove(self)
            return
        tiles = []
        for tile in stage.tiles:
            if (tile.inProximity(x, self.y, 40)):
                tiles += [tile]
        for tile in tiles:
            if (boxesIntersect(self.boundingBox, tile.boundingBox)):
                projectiles.remove(self)
                if (isinstance(tile, Save)):
                    return "save"
                return
