from cmu_112_graphics import *
from player import *
from stage import *
from audio import *
import time

def appStarted(app):
    app.player = Player(500, 500)
    app.keysPressed = {"a": False, "d": False, "w": False, "s": False, 
                       "Space": False, "f": False}
    app.timerDelay = 20
    app.FPS = 0
    app.start = 0
    app.kirbySprite = ImageTk.PhotoImage(app.loadImage("kirby.png"))
    app.stage = Stage(app.width, app.height, "stages/1.csv")
    app.paused = False
    app.audio = Audio()

def keyPressed(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = True
        if (event.key == "Space"):
            app.player.isJumping = True
    elif (event.key == "p"):
        app.paused = not app.paused
    elif (event.key == "x"):
        doStep(app)
    elif (event.key == "r"):
        appStarted(app)

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
    elif (app.keysPressed["d"]):
        app.player.setvx(10)
    else:
        app.player.setvx(0)
    if (app.player.isJumping):
        app.player.jump(app)
    app.player.move(app.stage)
    

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
    canvas.create_image(app.player.x, app.player.y, 
                        image = app.kirbySprite, anchor = "nw")
    for tile in app.stage.tiles:
        x0, y0, x1, y1 = tile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
    # print(app.player.onGround)
    renderBoundingBoxPoints(canvas, app.player.boundingBoxes)
    # renderTileBoxes(app, canvas)
    canvas.create_text(20, 20, font = "Arial 15 bold", fill = "teal", 
                        text = int(calculateFPS(app)))

def renderTileBoxes(app, canvas):
    for tile in app.stage.tiles:
        x0, y0, x1, y1 = tile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, width = 1, outline = "green")

def renderBoundingBoxPoints(canvas, boundingBoxes):
    for box in boundingBoxes:
        x0, y0, x1, y1 = boundingBoxes[box]
        canvas.create_rectangle(x0, y0, x1, y1, width = 1, outline = "green")


def main():
    runApp(width = 1200, height = 800)

if __name__ == '__main__':
    main()