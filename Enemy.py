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
        self.col = 0

    def getXpos(self):
        return self.x

    def getYpos(self):
        return self.y

    def keyPressed(self,app,event):
        if event.key == 'Right':
            self.x -= 15
        elif event.key == 'Left':
            self.x += 15

    def timerFired(self,app):
        if self.kind == 'chilly': 
            self.x -= random.randint(4,7)
        elif self.kind == 'metaknight':
            self.x += random.randint(10,15)
        elif self.kind == 'monkey':
            self.x += random.randint(-4,6)
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
        
        elif self.kind == 'sparky':
            (x0,y0) = (self.x - 50, self.y - 50)
            (x1,y1) = (self.x + 50, self.y+50)

        return (x0,y0,x1,y1)

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
            elif self.kind == 'sparky':
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.sparky))
        
    def deductLife(self):
        self.lives -= 1
    
    

class Boss(Enemy):
    def __init__(self,kind,lives,x,y):
        super().__init__(kind,lives,x,y)
        self.movingRight = False
        self.movingLeft = False
        self.target = []
        self.lives = lives
        self.walk = True
        self.Crush = False
        self.Jump = False
        self.vy = 0
        self.up = 10
        self.ground = 550
        self.col = 0
    
    def movePlayer(self,app, dx):
        self.x += dx

    def getEnemyBounds(self):
        (x0,y0,x1,y1) = (0,0,0,0)
        (x0,y0) = (self.x - 50, self.y - 70)
        (x1,y1) = (self.x + 50, self.y + 50)
        return (x0,y0,x1,y1)
            
    def deductLife(self):
        self.lives -= 1
    
    def keyPressed(self,app,event):
        if event.key == 'Right':
            print('this is mov')
            self.x -= 15
        elif event.key == 'Left':
            self.x += 15

    def drawLives(self,canvas, lives):
        cx,cy = self.x, self.y - 75
        for i in range(lives):
            canvas.create_rectangle(cx+20*i,cy,cx+20*(i+1),cy+20,fill = 'orange')
        canvas.create_text(cx-10,cy+10,text = f'{self.lives} x', fill = 'black')

    def patrol(self,app):
        distance = self.target.getX() - self.getXpos()
        if abs(distance) < 200:
            if distance < 0: 
                self.movingLeft = True
                self.movingRight = False
                self.slam(app)
                self.movePlayer(app,-1*random.randint(1, 5))
            else:
                self.movingRight = True
                self.movingLeft = False
                self.slam(app)
                self.movePlayer(app,random.randint(1, 5))

    def jump(self,app):
        if self.target.jumping == True and self.y > 0:
            self.Jump = True
            self.up = self.target.y-self.ground
            self.vy += self.up
            if self.movingLeft == True:
                self.movePlayer(app,-1*random.randint(1, 5))
            else:
                self.movePlayer(app,-1*random.randint(1, 5))
            self.Jump = False
        else:
            self.Jump = False

    def slam(self,app):
        self.Crush = True
        distance = self.target.getX() - self.getXpos()
        if abs(distance) < 100 and self.target.attacking == False:
            self.target.lives -= 1

    def timerFired(self,app):
        self.patrol(app)
        if (self.y > 0):
            if self.vy != 0:
                self.y -= self.vy
            if (self.y >= app.height*0.75) or self.y - self.vy > app.height*0.75:
                self.vy = 0
            else:
                self.vy -= 3
                self.y -= self.vy
        else:
            self.y = 50
            self.vy = 0

    def redrawAll(self,app,canvas):
        if self.Jump == True:
            canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.kingJump))   
        elif self.Crush == True:
            if self.movingLeft:
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.kingCrush))
            else:
                canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.kingCrushR))
        else:
            canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(app.king))
        self.drawLives(canvas,self.lives)

