from cmu_112_graphics import *
import random 
from Kirby import *
class Enemy:
    def __init__(self,kind,lives,x,y):
        self.lives = lives
        self.x = x
        self.y = y
        self.kind = kind
        self.spriteCounter = 0
        self.eaten = False
        self.vy = 6

    def getXpos(self):
        return self.x

    def getYpos(self):
        return self.y

    def timerFired(self,app):
        if self.kind == 'chilly': 
            self.x -= 5
        elif self.kind == 'metaknight':
            self.x += 10
        elif self.kind == 'monkey':
            self.y = random.randint(0,800)
            self.x = random.randint(0,1000)
        elif self.kind == 'bat':
            self.x = random.randint(0,800)
            self.y = app.height/2
        if self.vy != 0:
            self.y -= self.vy
        if self.y == app.height*0.8 or self.y - self.vy > app.height*0.8:
            self.vy = 0
        else:
            self.vy -= 2
            self.y -= self.vy
            
    def getEnemyBounds(self):
        (x0,y0,x1,y1) = (0,0,0,0)
        if self.kind == 'chilly':
            (x0,y0) = (self.x - 40, self.y - 70)
            (x1,y1) = (self.x + 40, self.y + 20)
            
        elif self.kind == 'metaknight':
            (x0,y0) = (self.x - 100, self.y - 90)
            (x1,y1) = (self.x + 40, self.y)
        
        elif self.kind == 'monkey':
            (x0,y0) = (self.x - 50, self.y - 50)
            (x1,y1) = (self.x + 50, self.y+50)

        elif self.kind == 'bat':
            (x0,y0) = (self.x - 70, self.y - 40)
            (x1,y1) = (self.x + 70, self.y+40)

        return (x0,y0,x1,y1)

    def loadAnimatedGif(self,path):
        spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
        i = 1
        while True:
            try:
                spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
                i += 1
            except Exception as e:
                return spritePhotoImages

    def redrawAll(self,app, canvas):
        if self.lives > 0 and self.eaten == False:
            if self.kind == 'metaknight':
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.metaknight))
            elif self.kind == 'chilly':
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.chilly))
            elif self.kind == 'monkey':
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.monkey))
            elif self.kind == 'bat':
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.bat))
        
    def deductLife(self):
        self.lives -= 1
    
    

class Boss(Enemy):
    def __init__(self,kind,lives,x,y):
        super().__init__(kind,lives,x,y)
        self.movingRight = False
        self.movingLeft = False
        self.target = []
        self.lives = 5
    
    def movePlayer(self,app, dx):
        self.x += dx

    def patrol(self,app):
        distance = self.target.getX() - self.getXpos()
        if abs(distance) < 200:
            if distance < 0: 
                self.movingLeft = True
                self.movingRight = False
                self.movePlayer(app,-1*random.randint(3, 9))
            else:
                self.movingRight = True
                self.movingLeft = False
                self.movePlayer(app,random.randint(3, 9))

    # def jump(self,app):
    
    # def slam(self,app):

    def timerFired(self,app):
        self.patrol(self)
        if self.vy != 0:
            self.y -= self.vy
        if self.y == app.height*0.75 or self.y - self.vy > app.height*0.75:
            self.vy = 0
        else:
            self.vy -= 2
            self.y -= self.vy

    # def redrawAll(self,app,canvas):
    #     canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.kingD))



