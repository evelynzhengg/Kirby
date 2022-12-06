from cmu_112_graphics import *
# https://www.newgrounds.com/art/view/mr300milesof/kirby-sprites-so-far
def appStarted(app):
    spritestrip = app.loadImage('kirbysprites.png')
    app.sprites = []
    for i in range(12):
        sprite = spritestrip.crop((28*i, 28, 35*i, 50))
        app.sprites.append(sprite)
    app.spriteCounter = 0

def timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)

def redrawAll(app, canvas):
    sprite = app.sprites[app.spriteCounter]
    canvas.create_image(200, 200, image=ImageTk.PhotoImage(sprite))


runApp(width=400, height=400)