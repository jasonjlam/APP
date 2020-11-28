import time

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = 48
        self.h = 44
        self.jumpVelocity = -30
        self.onGround = True
        self.isJumping = False
        self.doubleJump = False
        self.radius = 25
        self.updateBoundingBoxPoints(x, y)

    def jump(self, app):
        if (self.onGround):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.onGround = False
        elif (not self.doubleJump and not self.isJumping ):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.isJumping = True
            self.doubleJump = True


    def setvx(self, vx):
        self.vx = vx

    def move(self, stage):
        start = time.time()
        # print (self.vx, self.vy)
        # print(self.onGround)
        # print(self.doubleJump)
        print(self.vy)
        if (self.vy < 0):
            self.onGround = False
        self.moveJump()
        tiles = []
        for tile in stage.tiles:
            if (tile.inProximity(self.x, self.y, self.radius)):
                tiles.append(tile)
        x, y = self.moveWithCollision(stage, self.vx, self.vy, tiles)
        self.x += x
        self.y += y
        self.updateBoundingBoxPoints(self.x, self.y)
        # print (time.time() - start)
    
    def moveWithCollision(self, stage, vx, vy, tiles):
        if (vx == 0 and vy == 0):
            return (0, 0)
        vLength = int((vx ** 2 + vy ** 2) ** 0.5)
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
            if (collisions["x"] or collisions["y"]):
                currentVX -= xStep
                currentVY -= yStep
                if (collisions["x"]):
                    vx = currentVX
                    self.vx = 0
                if (collisions["y"]):
                    vy = currentVY
                    self.vy = 0
                return (vx, vy)
        self.vx = vx
        self.vy = vy
        return (vx, vy)

    def checkCollisions(self, stage, vx, vy, tiles):
        collisions = {"x": False, "y": False}
        self.updateBoundingBoxPoints(self.x + vx, self.y + vy)
        bBox = self.boundingBoxPoints
        collisionPoints = []
        for tile in tiles:
            for i in range(len(bBox)):
                x, y = bBox[i]
                if tile.isInTile(x,y):
                    collisionPoints += [i] 
        # print(collisionPoints)
        # 0 = middle left, 1 = bottom left, 2 = bottom right, 3 = middle right,
        # 4 = top right corner, 5 = top right, 6 = top left, 
        # 7 = top left corner
        self.checkGround(vx, vy, collisionPoints)
        if (5 in collisionPoints or 6 in collisionPoints):
            collisions["y"] = True
        if (4 in collisionPoints or 7 in collisionPoints
            or 5 in collisionPoints or 6 in collisionPoints):
            if (vy < 0):
                collisions["y"] = True
            else:
                collisions["x"] = True
        if ((0 in collisionPoints and 1 in collisionPoints) 
            or (2 in collisionPoints and 3 in collisionPoints)):
            collisions["x"] = True
        if ((1 in collisionPoints and 0 not in collisionPoints) 
            or (2 in collisionPoints and 3 not in collisionPoints)):
            if (vy < 0):
                collisions["x"] = True
            collisions["y"] = True
        if (0 in collisionPoints or 3 in collisionPoints):
            collisions["x"] = True
        return collisions

    def checkGround(self, vx, vy, collisionPoints):
        grounded = (1 in collisionPoints 
                        or 2 in collisionPoints and vy < 0)
        if (grounded):
            print("ON THE GROUND")
            self.doubleJump = False
            self.onGround = grounded

    def updateBoundingBoxPoints(self, x, y):
        self.boundingBoxPoints = [(0 + x, 30 + y), (2 + x, 40 + y), 
                        (44 + x, 40 + y), (46 + x, 30 + y), (42 + x, 4 + y), 
                        (30 + x, 0 + y), (16 + x, 0 + y), (6 + x, 4 + y)]


    def moveJump(self):
        if (self.vy < -9 and not self.isJumping):
            self.vy = -9
            self.onGround = False
        if (self.y > 500):
            self.onGround = True
            self.doubleJump = False
            self.y = 500
        if (not self.onGround):
            self.vy += 2.5
        if (self.vy > 20):
            self.vy = 20

