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
        self.jumpVelocity = -27
        self.onGround = True
        self.platform = None
        self.isJumping = False
        self.jumps = 2
        self.updateBoundingBoxes(0,0)
        self.doubleJumpPrimed = False
        self.facing = 1
        self.projectiles = []
        self.death = False
        self.godMode = False

    def shoot(self):
        if (len(self.projectiles) < 5):
            offset = 25
            self.projectiles += [PlayerProjectile(self.x + offset + 
                self.facing * offset, self.y + 15, self.facing * 16)]

    def jump(self, app):
        # print(self.doubleJumpPrimed)
        if (self.jumps > 1 and self.vy > -3 or 
            (self.jumps > 0  and self.vy > -3 and self.doubleJumpPrimed)):
            app.audio.playAudio("jump")
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
        if (not self.godMode):
            for entity in stage.getEntities():
                if (entity.inProximity(self.x + 25, self.y + 25)):
                    if (entity.isTouching(self.boundingBoxes)):
                        self.death = True
        self.groundCheck(stage, tiles)
        # print(self.x, self.y)
        self.moveWithCollision(stage, self.vx, self.vy, tiles)
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
        


    def moveWithCollision(self, stage, vx, vy, tiles, depth = 0):
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
            collisions = self.checkCollisions(stage, currentVX, currentVY, tiles)
            for key in collisions:
                if (collisions[key]):
                    currentVX -= xStep
                    currentVY -= yStep
                    if ((collisions["left"] or collisions["right"]) 
                                            and vx != 0):
                        self.vx = 0
                        self.x += currentVX
                        if (depth < 1):
                            self.moveWithCollision(stage, 0, vy, tiles, 1)
                        else:
                            self.y += currentVY
                        return
                    if ((collisions["top"] or collisions["bot"]) and vy != 0):
                        self.vy = 0
                        self.y += currentVY
                        if (depth < 1):
                            self.moveWithCollision(stage, vx, 0, tiles, 1)
                        else:
                            self.x += currentVX
                        return 
        self.vx = vx
        self.vy = vy
        self.x += vx
        self.y += vy

    def checkCollisions(self, stage, vx, vy, tiles):
        # print("Collisions being checked")
        # print(tiles)
        collisions = {"top": False, "left": False, "right": False, "bot": False,
         "platform": False}
        self.updateBoundingBoxes(self.x + vx, self.y + vy)
        boundingBox = self.boundingBoxes
        for tile in tiles:
            if (vy >= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["bot"])):
                    if (isinstance(tile, VanishingTile)):
                        tile.timer += 1
                    collisions["bot"] = True
                    if (isinstance(tile, MovingPlatform)):
                        self.platform = tile
            if (vy <= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["top"])):
                    collisions["top"] = True
                    if (isinstance(tile, VanishingTile)):
                        tile.timer += 1
            if (vx <= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["left"])):
                    collisions["left"] = True
                    if (isinstance(tile, VanishingTile)):
                        tile.timer += 1
            elif (vx >= 0):
                if (boxesIntersect(tile.boundingBox, 
                                        boundingBox["right"])):
                    collisions["right"] = True
                    if (isinstance(tile, VanishingTile)):
                        tile.timer += 1
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
        "bot": (1  + x, 20 + y, 46 + x, 41 + y)}

    def checkBorders(self, stage):
        if (self.x < -25):
            self.x = -25
        elif (self.x > stage.width - 25):
            self.x = -23
            return True
        elif (self.y < -25):
            self.y = -25
        elif (self.y > stage.height - 25):
            self.y = stage.height - 25

class PlayerProjectile(object):
    def __init__(self, x, y, vx):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.displayed = True
    def __hash__(self):
        return hash(self.x, self.y, self.vx)

    def __repr__(self):
        return f"Projectile at ({self.x}, {self.y}), velocity = {self.vx}"

    def move(self, app):
        if (not self.displayed):
            app.player.projectiles.remove(self)
        projectiles = app.player.projectiles
        stage = app.stage
        self.x += self.vx
        if (self.x < 0 or self.x > stage.width):
            self.displayed = False
            return
        tiles = []
        for entity in stage.getEntities():
            if (entity.inProximity(self.x, self.y, 40)):
                if (entity.hp > 0 and entity.isProjectileTouching(
                    self.x, self.y, self.r)):
                    entity.hp -= 1
                    self.displayed = False
        for tile in stage.tiles:
            if (tile.inProximity(self.x, self.y, 40)):
                if (boxIntersectsCircle(tile.boundingBox, self.x, self.y,
                    self.r)):
                    self.displayed = False
                    if (isinstance(tile, Save)):
                        return "save"
                    return

    def drawBoundingBox(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r,
        self.x + self.r, self.y + self.r, outline = "green")
        
