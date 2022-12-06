from cmu_112_graphics import *
import random 
from Enemy import *

class Block:
    def __init__(self,kind,x,y):
        self.x = x
        self.y = random.randint(y-200,y+200) 
        self.kind = kind
        self.blockWidth = 110
        self.blockHeight = 20
        self.blocks = random.randint(7,12)
        self.blockSpacing = 200
        self.enemyTypes = ['chilly','metaknight','monkey','bat','sparky']
        self.newE = Enemy(self.enemyTypes[random.randint(0,4)],1,self.x,self.y)
        self.scrollX = 0
    
    def getBlockBounds(self,app):
        (x0,y0) = (self.x-self.blockWidth/2.75-app.scrollX, (self.y - self.blockHeight*2.25))
        (x1,y1) = (self.x + self.blockWidth/2-app.scrollX, (self.y-self.blockHeight))
        return (x0,y0,x1,y1)


    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        canvas.create_image(self.x-app.scrollX, self.y, image=ImageTk.PhotoImage(app.block))
        self.scrollX = app.scrollX

class badBlock(Block):
    def __init__(self,kind,x,y):
        super().__init__(kind,x,y)
        self.touched = False
        self.blockWidth = 50
        self.blockHeight = 50
        self.newEnemies = []

    def getBlockBounds(self,app):
        (x0,y0) = (self.x-self.blockWidth/1.5-app.scrollX, (self.y - self.blockHeight*1.75))
        (x1,y1) = (self.x + self.blockWidth/1.5-app.scrollX, (self.y - self.blockHeight/2))
        return (x0,y0,x1,y1)

    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        if self.touched == False:
            canvas.create_image(self.x-app.scrollX,self.y, image=ImageTk.PhotoImage(app.badBlock))
        else:
            self.newE.redrawAll(app,canvas)
            self.newE.timerFired(app)

class lifeBlock(Block):
    def __init__(self,kind,x,y):
        super().__init__(kind,x,y)
        self.claimed = False
        self.blockWidth = 50
        self.blockHeight = 50
        self.added = False

    def getBlockBounds(self,app):
        (x0,y0) = (self.x-self.blockWidth/1.5-app.scrollX, (self.y - self.blockHeight*1.5))
        (x1,y1) = (self.x + self.blockWidth/1.5-app.scrollX, (self.y))
        return (x0,y0,x1,y1)

    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        if self.claimed == False:
            canvas.create_image(self.x-app.scrollX, self.y, image=ImageTk.PhotoImage(app.lifeBlock))

class hideBlock(Block):
    def __init__(self,kind,x,y):
        super().__init__(kind,x,y)
        self.claimed = False
        self.blockWidth = 50
        self.blockHeight = 50

    def getBlockBounds(self,app):
        (x0,y0) = (self.x-self.blockWidth-app.scrollX, (self.y - self.blockHeight*1.5))
        (x1,y1) = (self.x + self.blockWidth/1.5-app.scrollX, (self.y))
        return (x0,y0,x1,y1)

    def redrawAll(self,app,canvas):
        super().redrawAll(app,canvas)
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        if self.claimed == False:
            canvas.create_image(self.x-app.scrollX, self.y, image=ImageTk.PhotoImage(app.mystery))
            self.claimed == True

class Portal(Block):
    def __init__(self,kind,x,y):
        self.kind = kind
        self.x = x
        self.y = y
        self.claimed = False
        self.blockWidth = 50
        self.blockHeight = 50           

    def getBlockBounds(self,app):
        (x0,y0) = (self.x-self.blockWidth-app.scrollX, (self.y - self.blockHeight*1.5))
        (x1,y1) = (self.x + self.blockWidth/1.5-app.scrollX, (self.y))
        return (x0,y0,x1,y1)
    
    def redrawAll(self,app,canvas):
        super().redrawAll(app,canvas)
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        if self.claimed == False:
            canvas.create_rectangle(x0,y0,x1,y1,fill = 'black')
            self.claimed == True

    

