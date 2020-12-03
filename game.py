from cmu_112_graphics import *
from player import *
from stages import *
from audio import *
import time

def appStarted(app, x = 100, y = 700, stage = 1):
    app.player = Player(x, y)
    app.keysPressed = {"a": False, "d": False, "w": False, "s": False, 
                       "Space": False, "f": False, "Enter": True, "b": False}
    app.saveStage = stage
    app.saveX = x
    app.saveY = y
    app.timerDelay = 20
    app.FPS = 0
    app.start = 0
    app.kirbySprite = ImageTk.PhotoImage(app.loadImage("kirby.png"))
    app.currentStage = stage
    app.stage = createStage(stage, app.width, app.height)
    app.paused = False
    app.showBoundingBoxes = False
    app.audio = Audio()

def keyPressed(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = True
        if (event.key == "Enter"):
            app.player.shoot()
        if (event.key == "Space"):
            app.player.isJumping = True
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
    if (app.keysPressed["a"]):
        app.player.setvx(-10)
        app.player.facing = -1
    elif (app.keysPressed["d"]):
        app.player.setvx(10)
        app.player.facing = 1
    else:
        app.player.setvx(0)

    if (app.player.isJumping):
        app.player.jump(app)
    border = app.player.move(app.stage)
    for tile in app.stage.movingTiles:
        tile.move()
        print(tile.boundingBox)
    for projectile in app.player.projectiles:
        if (projectile.move(app) == "save"):
            recordSave(app)
    if (border != 0):
        changeStage(app, border)

def recordSave(app):
    app.saveX = app.player.x
    app.saveY = app.player.y
    app.saveStage = app.currentStage

def changeStage(app, border):
    print(border)
    app.currentStage += border
    print(app.currentStage)
    app.stage = createStage(app.currentStage, app.width, app.height)
    print(app.stage)


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
    renderCharacter(app, canvas)
    for tile in app.stage.getTiles():
        x0, y0, x1, y1 = tile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
    if (app.showBoundingBoxes):
        renderBoundingBoxes(app, canvas)
    canvas.create_text(20, 20, font = "Arial 15 bold", fill = "teal", 
                        text = int(calculateFPS(app)))
    canvas.create_text(30, 500, font = "Arial 15 bold", 
                        text = app.player.onPlatform)

def renderCharacter(app, canvas):
    for projectile in app.player.projectiles:
        x = projectile.x
        y = projectile.y
        r = projectile.r
        canvas.create_oval(x - r, y - r, x + r, y + r, fill = "yellow")
    canvas.create_image(app.player.x, app.player.y, 
                        image = app.kirbySprite, anchor = "nw")

def renderBoundingBoxes(app, canvas):
    for tile in app.stage.getTiles():
        x0, y0, x1, y1 = tile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, width = 1, outline = "green")
    for box in app.player.boundingBoxes:
        x0, y0, x1, y1 = app.player.boundingBoxes[box]
        canvas.create_rectangle(x0, y0, x1, y1, width = 1, outline = "green")
    for projectile in app.player.projectiles:
        x0, y0, x1, y1 = projectile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, width = 1, outline = "green")


def main():
    runApp(width = 1200, height = 800)

if __name__ == '__main__':
    main()