from cmu_112_graphics import *

def appStarted(app):
    app.playerX = app.width // 2
    app.playerY = app.width // 2
    app.kirbySprite = app.loadImage("kirby.png")
    app.keysPressed = {"a": False, "d": False, "w": False, "s": False}
    app.timerDelay = 25

def keyPressed(app, event):
    if (event.key == "a"):
        app.keysPressed["a"] = True
    elif (event.key == "d"):
        app.keysPressed["d"] = True
    elif (event.key == "w"):
        app.keysPressed["w"] = True
    elif (event.key == "s"):
        app.keysPressed["s"] = True

def keyReleased(app, event):
    if (event.key == "a"):
        app.keysPressed["a"] = False
    elif (event.key == "d"):
        app.keysPressed["d"] = False
    elif (event.key == "w"):
        app.keysPressed["w"] = False
    elif (event.key == "s"):
        app.keysPressed["s"] = False

def timerFired(app):
    doStep(app)

def doStep(app):
    print (app.keysPressed)
    if (app.keysPressed["a"]):
        app.playerX -= 10
    if (app.keysPressed["d"]):
        app.playerX += 10
    if (app.keysPressed["w"]):
        app.playerY -= 10
    if (app.keysPressed["s"]):
        app.playerY += 10



def redrawAll(app, canvas):
    canvas.create_image(app.playerX, app.playerY, 
                        image=ImageTk.PhotoImage(app.kirbySprite))

def main():
    runApp(width = 1000, height = 1000)

if __name__ == '__main__':
    main()