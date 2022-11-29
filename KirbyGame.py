from cmu_112_graphics import *
import random
from Kirby import *
from Enemy import *
from Block import *

# def appStarted(app):
#     app.counter = 0
#     startP = 'https://assets.nintendo.com/image/upload/c_fill,w_1200/q_auto:best/f_auto/dpr_2.0/ncom/en_US/games/switch/k/kirby-and-the-forgotten-land-switch/hero'
#     app.startPage = app.loadImage(startP)


# def timerFired(app):
#     app.counter += 1

# def redrawAll(app, canvas):
#     canvas.create_image(app.width//2,app.height//4, 
#                     image=ImageTk.PhotoImage(app.startPage))
#     canvas.create_text(app.width//2, app.height//2,
#                        text='Press control-q to begin', fill='black',
#                        font = ('Ariel',40))
# runApp(width = 1000,height = 800)

def appStarted(app):
    url = 'https://bghq.com/bgs/gba/k/knd/001.png'
    app.back1 = app.loadImage(url)
    app.back1 = app.scaleImage(app.back1,6)
    app.spriteCounter = 0
    app.scrollMargin = 100
    app.isGameOver = False
    app.scrollX = 0
    app.normBlocks = []
    app.enemy1 = Enemy('chilly.gif',1,800,500)
    app.enemy2 = Enemy('metaknight.gif',1,-300,500)
    app.enemy3 = Boss('kingD.gif',1,1000,500)   
    app.kirb = Kirby('normal',3,500,500)
    app.kirb.nearbyEnemies.append(app.enemy1)
    app.kirb.nearbyEnemies.append(app.enemy2)
    app.kirb.nearbyEnemies.append(app.enemy3)
    app.bounds = app.kirb.getKirbyBounds()
    app.enemy3.target = app.kirb
    app.badBlocks = []
    for i in range(1):
        app.normBlocks.append(Block('normal',300,400))  

# def makeBackVisible(app):
#     if (app.backX < app.scrollX + app.scrollMargin):
#         app.scrollX = app.backX - app.scrollMargin
#     if (app.backX > app.scrollX + app.width - app.scrollMargin):
#         app.scrollX = app.backX - app.width + app.scrollMargin

# def moveBack(app, dx, dy):
#     app.backX -= dx
#     makeBackVisible(app)

def timerFired(app):
    app.kirb.timerFired(app)
    if app.kirb.lives == 0:
        app.isGameOver = True

def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

def keyPressed(app, event):
    app.kirb.keyPressed(app,event)
    if (event.key == "Left"):    
        app.scrollX -= 5
        for block in app.normBlocks:
            block.x -= 5
    elif (event.key == "Right"): 
        app.scrollX += 5
        for block in app.normBlocks:
            block.x -= 5

def boundsIntersect(app, boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
        (ax0, ay0, ax1, ay1) = boundsA
        (bx0, by0, bx1, by1) = boundsB
        return ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0))

def redrawAll(app, canvas):
    canvas.create_image(500,400, image=ImageTk.PhotoImage(app.back1))
    app.kirb.redrawAll(app,canvas)
    app.enemy1.redrawAll(app,canvas)
    app.enemy1.timerFired(app)
    app.enemy2.redrawAll(app,canvas)
    app.enemy2.timerFired(app)
    app.enemy3.redrawAll(app,canvas)
    app.enemy3.timerFired(app)
    canvas.create_rectangle(app.kirb.getX()-50,app.kirb.getY()-50,app.kirb.getX()+50,app.kirb.getY()+50,outline='black')
    canvas.create_rectangle(app.enemy1.getXpos()-50,app.enemy1.getYpos()-50,app.enemy1.getXpos()+50,app.enemy1.getYpos()+50,outline='black')
    
    for block in app.normBlocks:
        if boundsIntersect(app,block.getBlockBounds(),app.kirb.getKirbyBounds()):
            app.kirb.blocked = True


    if app.isGameOver:
        canvas.create_rectangle(app.width//4,app.height//4,
            3*app.width//4, 3*app.height//4,fill = 'black')
        canvas.create_text(app.width//2,app.height//2,fill = 'white',
            text ='GAME OVER!')


    # draw the dots, shifted by the scrollX offset
    for block in app.normBlocks:
        # block.x -= app.scrollX# <-- This is where we scroll each dot!!!
        block.redrawAll(app,canvas)

    # draw the instructions and the current scrollX
    x = app.width/2
    canvas.create_text(x, 20, text='Use arrows to move left or right',
                       fill='black')
    canvas.create_text(x, 40, text=f'app.scrollX = {app.scrollX}',
                       fill='black')



runApp(width=1000, height=800)

