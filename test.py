from cmu_112_graphics import *
from player import *
import time

def appStarted(app):
    app.player = Player(500, 500)
    app.keysPressed = {"a": False, "d": False, "w": False, "s": False, 
                       "Space": False, "f": False}
    app.timerDelay = 25
    app.FPS = 0
    app.start = 0
    app.kirbySprite = ImageTk.PhotoImage(app.loadImage("kirby.png"))

def keyPressed(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = True

def keyReleased(app, event):
    if ((event.key) in app.keysPressed):
        app.keysPressed[event.key] = False
        if (event.key == "Space"):
            app.player.isJumping = False

def timerFired(app):
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
        app.player.jump()
    app.player.move()

def calculateFPS(app):
    millisecond = 1000
    minFrame = app.timerDelay / millisecond
    snapshotFPS = 1 / (max(time.time() - app.start, minFrame))
    return snapshotFPS
    # Moving average
    # alpha = 0.8
    # beta = 0.2
    # return alpha * FPS + beta * snapshotFPS

def renderInitialImages(app, canvas):
    player = canvas.create_image(app.player.x, app.player.y, 
            image = app.kirbySprite)

def redrawAll(app, canvas):
    # if (len(canvas.find_all()) == 1):
    #     renderInitialImages(app, canvas)
    canvas.create_image(app.player.x, app.player.y, 
                        image = app.kirbySprite)
    # # canvas.create_rectangle(app.player.x, app.player.y, app.player.x + 10,
    # #                        app.player.y + 10)
    canvas.create_text(20, 20, font = "Arial 15 bold", 
                        text = int(calculateFPS(app)))

def main():
    runApp(width = 800, height = 600)

if __name__ == '__main__':
    main()