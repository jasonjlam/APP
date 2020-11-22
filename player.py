class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.onGround = True
        self.isJumping = False
        self.doubleJump = False
        self.boundingBoxPoints = [(0,8), (0, 20), (23, 20), (23, 8), (15, 0),
                                 (8, 0)]

    def jump(self):
        if (self.onGround):
            self.vy = -24
            self.isJumping = True
            self.onGround = False
        elif (not self.doubleJump and not self.isJumping ):
            self.vy = -24
            self.isJumping = True
            self.doubleJump = True


    def setvx(self, vx):
        self.vx = vx

    def move(self):
        # print (self.doubleJump)
        # print (self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy
        if (self.vy < -9 and not self.isJumping):
            self.vy = -9
        if (self.y > 500):
            self.onGround = True
            self.doubleJump = False
            self.y = 500
        if (not self.onGround):
            self.vy += 2.5