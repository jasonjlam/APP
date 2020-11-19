from cmu_112_graphics import *
from player import *

def appStarted(app):
    app.player = Player(500, 500)
    app.kirbySprite = app.loadImage("kirby.png")
    app.keysPressed = {"a": False, "d": False, "w": False, "s": False, 
                       "Space": False}
    app.timerDelay = 17

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



def redrawAll(app, canvas):
    canvas.create_image(app.player.x, app.player.y, 
                        image=ImageTk.PhotoImage(app.kirbySprite))

def main():
    runApp(width = 800, height = 600)

if __name__ == '__main__':
    main()