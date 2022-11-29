from cmu_112_graphics import *
import random 
from Enemy import *

class Block:
    def __init__(self,kind,x,y):
        self.x = random.randint(100,1000)
        self.y = random.randint(100,600)
        self.kind = kind
        self.blockWidth = random.randint(400,600)
        self.blockHeight = random.randint(30,50)
        self.blocks = random.randint(7,12)
        self.blockSpacing = 90
    
    def getBlockBounds(self):
        (x0,y0) = (self.x-self.blockWidth/2, self.y - self.blockHeight/2)
        (x1,y1) = (self.x + self.blockWidth/2, self.y + self.blockHeight/2)
        return (x0,y0,x1,y1)

    
    def redrawAll(self,app,canvas):
        (x0,y0,x1,y1) = self.getBlockBounds()
        canvas.create_rectangle(x0,y0,x1,y1,fill = "black")

class badBlock(Block):
    def __init__(self,kind,x,y):
        super().__init__()
        self.touched = False

    def spawn(self,app,canvas):
        if self.touched == True:
            enemyTypes = ['chilly.gif','metaknight.gif']
            newE = Enemy('chilly.gif',1,self.x,self.y)
            newE.redrawAll(app,canvas)
    
    def redrawAll(self,app,canvas):
        x0 = self.x-self.blockWidth/2
        x1 = self.x + self.blockWidth/2
        y0 = self.y - self.blockHeight/2
        y1 = self.y + self.blockHeight/2
        canvas.create_rectangle(x0,y0,x1,y1,fill = "orange")


    

