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
        # print(self.doubleJump)
        self.moveJump()
        if (self.vx == 0 and self.vy == 0):
            xAdjust, yAdjust = (0, 0)
        else:
            tiles = []
            for tile in stage.tiles:
                if (tile.inProximity(self.x, self.y, self.radius)):
                    tiles.append(tile)
            self.moveWithCollision(stage, self.vx, self.vy,
                                tiles, 0, 0)
        self.updateBoundingBoxPoints(self.x, self.y)
        # print (time.time() - start)
    
    def moveWithCollision(self, stage, vx, vy, tiles, xAdjust, yAdjust):
        self.updateBoundingBoxPoints(self.x + vx, self.y + vy)
        if (len(tiles) == 0):
            print(xAdjust, yAdjust)
            self.x += vx + xAdjust
            self.y += vy + yAdjust
            return
        tile = tiles[0]
        xBorder = False
        yBorder = False
        xContact = False
        if (self.x + vx - 5 < 0 or self.x + vx + self.w - 5 > stage.width):
            xAdjust = -vx
            xBorder = True
        if (self.y + vy - 5 < 0 or self.y + vy + self.h - 5 > stage.height):
            yAdjust = -vy
            yBorder = True
        collisionPoints = []
        sidePoints = [0, 3]
        vertPoints = [1, 2, 5, 6]
        cornerPoints = [4, 7]
        for i in range(len(self.boundingBoxPoints)):
            x, y = self.boundingBoxPoints[i]
            if (tile.isInTile(x,y)):
                collisionPoints.append(i)
        print (collisionPoints)
        if (1 in collisionPoints or 2 in collisionPoints
            and 0 not in collisionPoints and 3 not in collisionPoints):
            self.onGround = True
            self.doubleJump = False
        else:
            self.onGround = False
        for i in sidePoints:
            if (i in collisionPoints and not xBorder):
                print("Side")
                xContact = True
                xAdjust = tile.adjustBy(self.boundingBoxPoints[i], "x")
        for i in vertPoints:
            if (i in collisionPoints and not yBorder and not xContact):
                print("Vertical")
                x, y = self.boundingBoxPoints[i]
                yAdjust = tile.adjustBy(self.boundingBoxPoints[i], "y")
        for i in cornerPoints:
            if (i in collisionPoints and not xContact):
                xOffset = 1
                yOffset = 1
                x, y = self.boundingBoxPoints[i]
                print("Corner")
                if (abs(vx) > abs(vy)):
                    if (vx > 0 and not xBorder):
                        xAdjust = tile.adjustBy((x + xOffset, y), "x")
                    else:
                        xAdjust = tile.adjustBy((x - xOffset, y), "x")
                elif (not yBorder):
                    yAdjust = tile.adjustBy((x, y - yOffset), "y")
        self.moveWithCollision(stage, vx, vy, tiles[1:], xAdjust, yAdjust)
        

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
        if (self.vy > 10):
            self.vy = 10

