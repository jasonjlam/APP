class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.onGround = True
        self.isJumping = False

    def jump(self):
        if (self.onGround):
            self.vy = -20
            self.isJumping = True
            self.onGround = False

    def setvx(self, vx):
        self.vx = vx

    def move(self):
        # print (self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy
        if (self.vy < -11 and not self.isJumping):
            self.vy = -11
        if (self.y > 500):
            self.onGround = True
            self.y = 500
        if (not self.onGround):
            self.vy += 3