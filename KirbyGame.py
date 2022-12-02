from cmu_112_graphics import *
import random
from Kirby import *
from Enemy import *
from Block import *

def appStarted(app):
    app.counter = 0
    startP = 'https://assets.nintendo.com/image/upload/c_fill,w_1200/q_auto:best/f_auto/dpr_2.0/ncom/en_US/games/switch/k/kirby-and-the-forgotten-land-switch/hero'
    app.startPage = app.loadImage(startP) #this image was taken from the url above set to startP


def timerFired(app):
    app.counter += 1

def redrawAll(app, canvas):
    canvas.create_image(app.width//2,app.height//4, 
                    image=ImageTk.PhotoImage(app.startPage))
    canvas.create_text(app.width//2, app.height//2,
                       text='Press control-q to begin', fill='black',
                       font = ('Ariel',40))
runApp(width = 1000,height = 800)

def appStarted(app):
    url = 'https://bghq.com/bgs/gba/k/knd/001.png' #this image was taken from https://bghq.com/bgs/gba/k/knd/001.png
    app.back1 = app.loadImage(url)
    app.back1 = app.scaleImage(app.back1,6)
    app.spriteCounter = 0
    app.scrollMargin = 100
    app.isGameOver = False
    app.scrollX = 0
    app.normBlocks = []
    app.enemy1 = Enemy('chilly',1,800,500)
    app.enemy2 = Enemy('metaknight',1,-300,500)
    app.enemy3 = Enemy('monkey',1,1000,500)
    app.float = app.scaleImage(app.loadImage('fly.png'),3) #all sprites were hand drawn on https://www.pixilart.com/draw/kingd-sr2686c7792a4ae
    app.floatL = app.float.transpose(Image.FLIP_LEFT_RIGHT)
    app.walk = app.scaleImage(app.loadImage('walk.png'),3)
    app.walkL = app.walk.transpose(Image.FLIP_LEFT_RIGHT)
    app.suck = app.scaleImage(app.loadImage('inhale.png'),3)
    app.suckL = app.suck.transpose(Image.FLIP_LEFT_RIGHT)
    app.fight = app.scaleImage(app.loadImage('attack.png'),3)
    app.fightL = app.fight.transpose(Image.FLIP_LEFT_RIGHT)
    app.knight = app.scaleImage(app.loadImage('knight.png'),3)
    app.knightR = app.knight.transpose(Image.FLIP_LEFT_RIGHT)
    app.chilly = app.scaleImage(app.loadImage('chilly.png'),3)
    app.metaknight = app.scaleImage(app.loadImage('metaknight.png'),3)
    app.bat = app.scaleImage(app.loadImage('bat.png'),3)
    app.monkey = app.scaleImage(app.loadImage('monkey.png'),3)
    app.kingD = ''
    app.kirb = Kirby('normal',3,500,app.height*0.8)
    app.kirb.nearbyEnemies.append(app.enemy1)
    app.kirb.nearbyEnemies.append(app.enemy2)
    app.kirb.nearbyEnemies.append(app.enemy3)
    app.bounds = app.kirb.getKirbyBounds(app)
    app.enemy3.target = app.kirb
    app.badBlocks = []
    app.lifeBlocks = 2
    app.collected = 0
    app.blocks = []
    app.ready = False
    app.level = 1
    for i in range(app.level*2):
        app.blocks.append((Block('normal',(i+1)*300,400)))
    for i in range(app.level*3):
        app.blocks.append((badBlock('normal',(i+1)*400,400))) 
    for i in range(app.level*2):
        app.blocks.append((lifeBlock('normal',(i+1)*250,400))) 

def addBlock(app):
    if app.scrollX == 300:
        app.level += 1
        app.blocks = []
        for i in range(app.level*2):
            app.blocks.append((Block('normal',(i+1)*300,400)))
        for i in range(app.level*3):
            app.blocks.append((badBlock('normal',(i+1)*400,400))) 
        for i in range(app.level*2):
            app.blocks.append((lifeBlock('normal',(i+1)*250,400))) 
            app.lifeBlocks += app.level*2
        app.scrollX = 0


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
    addBlock(app)
    app.ready = (app.collected == app.lifeBlocks and app.level == 3)


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
    (x0,y0,x1,y1) = app.blocks[0].getBlockBounds(app)
    canvas.create_rectangle(x0,y0,x1,y1,outline='orange', width = 5)
    # canvas.create_rectangle(app.enemy2.getXpos()-100,app.enemy2.getYpos()-90,app.enemy2.getXpos()+40,app.enemy2.getYpos(),outline='black')


    # draw the dots, shifted by the scrollX offset
    for block in app.blocks:
        block.redrawAll(app,canvas)


    # draw the instructions and the current scrollX
    x = app.width/2
    canvas.create_text(x, 20, text='Use arrows to move left or right',
                       fill='black')
    canvas.create_text(x, 40, text=f'app.scrollX = {app.scrollX}',
                       fill='black')
    print(app.collected)
    print(app.lifeBlocks)
    if app.kirb.lives == 10:
        canvas.create_rectangle(app.width//4,app.height//4,
            3*app.width//4, 3*app.height//4,fill = 'purple')
        canvas.create_text(app.width//2,app.height//2,fill = 'white',
            text ='Congrats! You have collected enough life blocks! You are ready for battle.')

    if app.isGameOver:
        canvas.create_rectangle(app.width//4,app.height//4,
            3*app.width//4, 3*app.height//4,fill = 'black')
        canvas.create_text(app.width//2,app.height//2,fill = 'white',
            text ='GAME OVER!')

runApp(width=1000, height=800)

def appStarted(app):
    app.boss = Boss('kingD',5,200,200)
    app.kirb = Kirby('normal',10,500,app.height*0.8)
    app.kirb.moveR = 40
    app.kirb.moveL = 40
    app.float = app.scaleImage(app.loadImage('fly.png'),3)
    app.floatL = app.float.transpose(Image.FLIP_LEFT_RIGHT)
    app.walk = app.scaleImage(app.loadImage('walk.png'),3)
    app.walkL = app.walk.transpose(Image.FLIP_LEFT_RIGHT)
    app.suck = app.scaleImage(app.loadImage('inhale.png'),3)
    app.suckL = app.suck.transpose(Image.FLIP_LEFT_RIGHT)
    app.fight = app.scaleImage(app.loadImage('attack.png'),3)
    app.fightL = app.fight.transpose(Image.FLIP_LEFT_RIGHT)
    app.knight = app.scaleImage(app.loadImage('knight.png'),3)
    app.knightR = app.knight.transpose(Image.FLIP_LEFT_RIGHT)
    app.chilly = app.scaleImage(app.loadImage('chilly.png'),3)
    app.metaknight = app.scaleImage(app.loadImage('metaknight.png'),3)
    app.bat = app.scaleImage(app.loadImage('bat.png'),3)
    app.monkey = app.scaleImage(app.loadImage('monkey.png'),3)
    app.kingJump = app.scaleImage(app.loadImage('kingDJump.png'),3)
    app.king = app.scaleImage(app.loadImage('kingD.png'),3)
    app.kingCrush = app.scaleImage(app.loadImage('kingDSmash.png'),3)
    app.kingCrushR = app.kingCrush.transpose(Image.FLIP_LEFT_RIGHT)
    back = 'bossFight.jpeg' #this image was taken from https://www.deviantart.com/princesskirbyswirl/art/The-Magalor-final-boss-fight-background-851147131
    app.background = app.loadImage(back)
    app.blocks = []
    for i in range(10):
        app.blocks.append((lifeBlock('normal',(i+1)*250,400))) 
    app.scrollX = 0
    app.isGameOver = False
    app.kirb.nearbyEnemies.append(app.boss)

def timerFired(app):
    app.kirb.timerFired(app)
    if app.kirb.lives == 0:
        app.isGameOver = True

def keyPressed(app, event):
    app.kirb.keyPressed(app,event)

def redrawAll(app, canvas):
    canvas.create_image(app.width//2,app.height//4, 
                image=ImageTk.PhotoImage(app.scaleImage(app.background,2.5)))
    app.boss.target = app.kirb
    app.boss.redrawAll(app,canvas)
    app.boss.timerFired(app)
    app.kirb.redrawAll(app,canvas)
    app.kirb.timerFired(app)
    for block in app.blocks:
        block.redrawAll(app,canvas)
    
    if app.isGameOver:
        canvas.create_rectangle(app.width//4,app.height//4,
            3*app.width//4, 3*app.height//4,fill = 'black')
        canvas.create_text(app.width//2,app.height//2,fill = 'white',
            text ='GAME OVER!')
    elif app.boss.lives == 0:
        canvas.create_rectangle(app.width//4,app.height//4,
            3*app.width//4, 3*app.height//4,fill = 'black')
        canvas.create_text(app.width//2,app.height//2,fill = 'white',
            text ='YOU WIN!')

runApp(width = 1000,height = 800)


