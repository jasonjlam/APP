# Main game

from cmu_112_graphics import *
from player import *
from stages import *
from audio import *
import time


def appStarted(app, x = 100, y = 700, stage = None):
    app.keysPressed = {"a": False, "d": False, "w": False, "s": False, 
                       "Space": False, "Enter": False}
    app.saveStage = stage
    app.saveX = x
    app.saveY = y
    app.timerDelay = 20
    app.FPS = 0
    app.start = 0
    app.currentFrame = 1
    initializeSprites(app)
    if (stage != None):
        print("went back to stage")
        app.stage = stage
        app.player = Player(x, y)
    else:
        app.stage = Stage(app.width, app.height, randint(12,17), randint(12,17))
        app.player = Player(-10, app.stage.startY * app.stage.tileSize - 42)
    app.paused = False
    app.showBoundingBoxes = False
    app.audio = Audio()

def initializeSprites(app):
    app.sprites = {}
    app.sprites["rightKirby"] = []
    app.sprites["leftKirby"] = []
    for i in range(1, 15):
        sprite = app.loadImage(f"assets/kirby/{i}.png")
        app.sprites["rightKirby"].append(ImageTk.PhotoImage(sprite))
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        app.sprites["leftKirby"].append(ImageTk.PhotoImage(sprite))
    app.sprites["haunter"] = []
    for i in range(25):
        haunter = app.loadImage(fr"assets/entities/haunter/{i + 1}.gif")
        haunter = app.scaleImage(haunter, 6)
        app.sprites["haunter"].append(ImageTk.PhotoImage(haunter))
    app.sprites["gastly"] = ImageTk.PhotoImage(app.loadImage(
            "assets/entities/gastly.png"))
    app.sprites["grassBackground"] = ImageTk.PhotoImage(app.loadImage(
        "assets/grassbackground.png"))
    for sprite in ["dirt", "grass"]:
        app.sprites[sprite] = ImageTk.PhotoImage(app.loadImage(
            f"assets/tiles/{sprite}.png"))

def keyPressed(app, event):
    if (not app.player.death):
        if (event.key == "Enter" and not app.keysPressed["Enter"]):
            app.player.shoot(app)
        if (event.key == "Space"):
            app.player.isJumping = True
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = True
    elif (event.key == "b"):
        app.showBoundingBoxes = not app.showBoundingBoxes
    elif (event.key == "g"):
        app.player.godMode = not app.player.godMode
    elif (event.key == "p"):
        app.paused = not app.paused
    elif (event.key == "x"):
        doStep(app)
    elif (event.key == "r"):
        appStarted(app, app.saveX, app.saveY, app.saveStage)

def keyReleased(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = False
        if (event.key == "Space"):
            app.player.isJumping = False
            if (app.player.jumps == 1):
                app.player.doubleJumpPrimed = True

def timerFired(app):
    if (not app.paused):
        doStep(app)

def doStep(app):
    app.start = time.time()
    # print (app.keysPressed)
    if (not app.player.death):
        if (app.keysPressed["a"]):
            app.player.vx = -10
            app.player.facing = -1
        elif (app.keysPressed["d"]):
            app.player.vx = 10
            app.player.facing = 1
        else:
            app.player.vx = 0
        if (app.player.isJumping):
            app.player.jump(app)
        for projectile in app.player.projectiles:
            if (projectile.move(app) == "save"):
                recordSave(app)
    else:
        app.player.vx = 0
        app.player.vy = 0
        app.player.onGround = True
    if (moveObjects(app)):
        app.stage = app.stage.generateNewStage()
    if (app.player.death):
        app.currentFrame = 14
    elif (not(app.player.onGround or app.player.platform != None)):
        if (app.player.vy < 0):
            app.currentFrame = 12
        else:
            app.currentFrame = 13
    elif (app.player.vx != 0):
        app.currentFrame += 0.5
        if (app.currentFrame > 11):
            app.currentFrame = 2
    else:
        app.currentFrame = 1

def moveObjects(app):
    for tile in app.stage.movingTiles:
        tile.move()
    for entity in app.stage.entities:
        if (entity.moving):
            entity.move(app)
    if (app.stage.boss != None):
        app.stage.boss.move(app)
    return app.player.move(app)

def recordSave(app):
    app.saveX = app.player.x
    app.saveY = app.player.y
    app.saveStage = app.stage


def calculateFPS(app):
    millisecond = 1000
    minFrame = app.timerDelay / millisecond
    snapshotFPS = 1 / (max(time.time() - app.start, minFrame))
    return snapshotFPS
    # Moving average
    # alpha = 0.8
    # beta = 0.2
    # return alpha * FPS + beta * snapshotFPS

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawCharacter(app, canvas)
    drawTiles(app, canvas)
    drawEntities(app, canvas)
    drawBoss(app, canvas)
    if (app.showBoundingBoxes):
        drawBoundingBoxes(app, canvas)
    canvas.create_text(20, 20, font = "Arial 15 bold", fill = "teal", 
                        text = int(calculateFPS(app)))
    if (app.player.death):
        canvas.create_text(app.width / 2, app.height / 2, 
            font = "Terminal 100 bold", fill = "red",
            text = "    You died!\nPress R to restart")
    # canvas.create_text(30, 500, font = "Arial 15 bold", 
    #                     text = str(app.player.platform))

def drawBackground(app, canvas):
    canvas.create_image(0, 0,  image = app.sprites["grassBackground"], 
        anchor = "nw")

def drawBoss(app, canvas):
    if (app.stage.boss == None):
        return
    else:
        app.stage.boss.draw(app, canvas)

def drawTiles(app, canvas):
    for tile in app.stage.getTiles():
        tile.draw(app, canvas)

def drawEntities(app, canvas):
    for entity in app.stage.entities:
        entity.draw(app, canvas)

def drawCharacter(app, canvas):
    adjust = 0
    if (app.currentFrame in [2, 7]):
        adjust = 2
    elif (app.currentFrame in [13]):
        adjust = 4
    for projectile in app.player.projectiles:
        x = projectile.x
        y = projectile.y
        r = projectile.r
        canvas.create_oval(x - r, y - r, x + r, y + r, fill = "yellow")
    if (app.player.facing == -1):
        canvas.create_image(app.player.x + adjust, app.player.y - adjust, 
            image = app.sprites["leftKirby"][int(app.currentFrame - 1)], anchor = "nw")
    else:
        canvas.create_image(app.player.x + adjust, app.player.y - adjust, 
            image = app.sprites["rightKirby"][int(app.currentFrame - 1)], anchor = "nw")
    if (app.player.godMode):
        canvas.create_text(app.player.x + app.player.w / 2, 
            app.player.y - 10, text = "Invincible")

def drawBoundingBoxes(app, canvas):
    for tile in app.stage.getTiles():
        x0, y0, x1, y1 = tile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, outline = "green")
    for box in app.player.boundingBoxes:
        x0, y0, x1, y1 = app.player.boundingBoxes[box]
        canvas.create_rectangle(x0, y0, x1, y1, outline = "green")
    for entity in app.stage.getEntities() + app.player.projectiles:
        entity.drawBoundingBox(canvas)


def main():
    runApp(width = 1600, height = 800, mvcCheck = False)

if __name__ == '__main__':
    main()