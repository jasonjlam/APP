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
    app.stage = Stage(app.width, app.height)
    app.paused = False
    app.audio = Audio()

def keyPressed(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = True
    elif (event.key == "p"):
        app.paused = not app.paused
    elif (event.key == "x"):
        doStep(app)

def keyReleased(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = False
        if (event.key == "Space"):
            app.player.isJumping = False

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
    if (app.keysPressed["Space"]):
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
    # if (len(canvas.find_all()) == 1):
    #     renderInitialImages(app, canvas)
    canvas.create_image(app.player.x, app.player.y, 
                        image = app.kirbySprite, anchor = "nw")
    # # canvas.create_rectangle(app.player.x, app.player.y, app.player.x + 10,
    # #                        app.player.y + 10)
    canvas.create_text(20, 20, font = "Arial 15 bold", 
                        text = int(calculateFPS(app)))
    for tile in app.stage.tiles:
        x0, y0, x1, y1 = tile.boundingBox
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
    # print(app.player.onGround)
    renderBoundingBoxPoints(canvas, app.player.boundingBoxPoints)

def renderBoundingBoxPoints(canvas, boundingBoxPoints):
    for i in range(len(boundingBoxPoints)):
        x, y = boundingBoxPoints[i]
        canvas.create_text(x, y, font = "Arial 8", 
                                fill = "purple", text = str(i))

def main():
    runApp(width = 800, height = 600)

if __name__ == '__main__':
    main()