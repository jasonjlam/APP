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
        self.onGround = False
        self.isJumping = False
        self.doubleJump = False
        self.radius = 25
        self.updateBoundingBoxPoints(x, y)

    def jump(self, app):
        if (self.onGround):
            app.audio.jumpAudio()
            self.vy = self.jumpVelocity
            self.isJumping = True
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
        print(vx, currentVX, vy, currentVY)
        currentStep = 0
        while (currentStep < vLength):
            currentStep += 1
            print(i)
            currentVX += xStep
            currentVY += yStep
            collisions = self.checkCollisions(stage, currentVX, 
                                        currentVY, tiles)
            if (collisions["x"] or collisions["y"]):
                print(f"{currentVX}/{vx}, {currentVY}/{vy}")
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
        print(collisionPoints)
        if ((1 in collisionPoints and 0 not in collisionPoints) 
            or (2 in collisionPoints and 3 not in collisionPoints)
            or 5 in collisionPoints or 6 in collisionPoints
            or 4 in collisionPoints or 7 in collisionPoints):
            collisions["y"] = True
        if (0 in collisionPoints or 3 in collisionPoints):
            collisions["x"] = True

        return collisions






    def updateBoundingBoxPoints(self, x, y):
        self.boundingBoxPoints = [(0 + x, 16 + y), (0 + x, 40 + y), 
                        (46 + x, 40 + y), (46 + x, 16 + y), (42 + x, 4 + y), 
                        (30 + x, 0 + y), (16 + x, 0 + y), (6 + x, 4 + y)]


    def moveJump(self):
        if (self.vy < -9 and not self.isJumping):
            self.vy = -9
        if (self.y > 500):
            self.onGround = True
            self.doubleJump = False
            self.y = 500
        if (not self.onGround):
            self.vy += 2.5
        if (self.vy > 20):
            self.vy = 20

