import time

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.onGround = True
        self.isJumping = False
        self.doubleJump = False
        self.radius = 25
        self.updateBoundingBoxPoints(x, y)

    def jump(self):
        if (self.onGround):
            self.vy = -12
            self.isJumping = True
            self.onGround = False
        elif (not self.doubleJump and not self.isJumping ):
            self.vy = -12
            self.isJumping = True
            self.doubleJump = True


    def setvx(self, vx):
        self.vx = vx


    def move(self, stage):
        start = time.time()
        # print (self.doubleJump)
        # print (self.vx, self.vy)
        xAdjust, yAdjust = self.moveWithCollision(stage, self.vx, self.vy)
        self.x += xAdjust + self.vx
        self.y += yAdjust + self.vy
        # self.moveJump()
        print (time.time() - start)
    
    def moveWithCollision(self, stage, vx, vy):
        self.updateBoundingBoxPoints(self.x + vx, self.y + vy)
        if (self.x + vx)
        for tile in stage.tiles:
            if (tile.inProximity(self.x, self.y, self.radius)):
                collisionPoints = []
                sidePoints = [0, 3]
                vertPoints = [1, 2, 5, 6]
                cornerPoints = [4, 7]
                for i in range(len(self.boundingBoxPoints)):
                    x, y = self.boundingBoxPoints[i]
                    if (tile.isInTile(x,y)):
                        collisionPoints.append(i)
                for i in sidePoints:
                    if (i in collisionPoints):
                        print("Side")
                        return (tile.adjustBy(
                                    self.boundingBoxPoints[i], "x"), 0)
                for i in vertPoints:
                    if (i in collisionPoints):
                        print("Vertical")
                        return (0, tile.adjustBy(
                                    self.boundingBoxPoints[i], "y"))
                for i in cornerPoints:
                    if (i in collisionPoints):
                        xOffset = 1
                        yOffset = 1
                        x, y = self.boundingBoxPoints[i]
                        print("Corner")
                        if (abs(vx) > abs(vy)):
                            if (vx > 0):
                                return (tile.adjustBy((x + xOffset, y), "x"), 0) 
                            else:
                                return (tile.adjustBy((x - xOffset, y), "x"), 0) 
                        else:
                            print("Y is bigger")
                            return (0, tile.adjustBy((x, y - yOffset), 
                                        "y")) 
        return (0, 0)

        if (xAdjust != 0):
            print("xAdjust", xAdjust)
        if (yAdjust != 0):
            print("yAdjust", yAdjust)
        self.x += xAdjust + vx
        self.y += yAdjust + vy


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

