from cmu_112_graphics import *
import random 
from Enemy import *

class Block:
    def __init__(self,kind,x,y):
        self.x = x
        self.y = random.randint(y-300,y+150) 
        self.kind = kind
        self.blockWidth = 100
        self.blockHeight = 50
        self.blocks = random.randint(7,12)
        self.blockSpacing = 200
        self.enemyTypes = ['chilly','metaknight','monkey','bat']
        self.newE = Enemy(self.enemyTypes[random.randint(0,3)],1,self.x,self.y)
        self.scrollX = 0
    
    def getBlockBounds(self,app):
        (x0,y0) = (self.x-self.blockWidth/2-app.scrollX, (self.y - self.blockHeight/2))
        (x1,y1) = (self.x + self.blockWidth/2-app.scrollX, (self.y + self.blockHeight/2))
        return (x0,y0,x1,y1)


    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        canvas.create_rectangle(x0,y0,x1,y1,fill = "beige",outline = 'black',width = 3)
        self.scrollX = app.scrollX

class badBlock(Block):
    def __init__(self,kind,x,y):
        super().__init__(kind,x,y)
        self.touched = False
        self.blockWidth = 75
        self.blockHeight = 75
        self.newEnemies = []

    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        if self.touched == False:
            canvas.create_rectangle(x0,y0,x1,y1,fill = "orange",outline = 'purple',
                                    width = 5)
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
    
    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds(app)
        if self.claimed == False:
            canvas.create_rectangle(x0,y0,x1,y1,fill = "red",outline = 'yellow',
                                    width = 5)



            

    


    

