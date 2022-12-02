from cmu_112_graphics import *
import math
from Block import *

class Kirby:
    def __init__(self,action,lives,x,y):
        self.action = action
        self.lives = lives
        self.x = x
        self.y = y
        self.float = ''
        self.walk = ''
        self.suck = ''
        self.fight = ''
        # self.knight = 'kirbyknight.gif'
        self.spriteCounter = 0
        self.jumping = False
        self.eating = False
        self.attacking = False
        self.slashing = True
        self.nearbyEnemies = []
        self.scrollX = 0
        self.scrollMargin = 20
        self.vy = 0
        self.moveR = 15
        self.moveL = 15
        self.up = 20
        self.ground = y
        self.topB = False
        self.added = False
        self.state = 'R'
        self.bounds = 0
        self.canL = True
        self.canR = True
        self.canU = True
        self.canJ = True
        self.goingDown = False

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getKirbyBounds(self,app):
        (x0,y0) = (self.x - 50, self.y - 70)
        (x1,y1) = (self.x + 40, self.y + 10)
        self.bounds = (x0,y0,x1,y1)
        return (x0,y0,x1,y1)

    def jump(self):
        self.jumping = True
        if self.canJ:
            self.vy += self.up

    def timerFired(self,app):
        self.eat()
        self.touched(app)
        self.punch(app)
        self.sword()
        self.getKirbyBounds(app)
        if self.vy != 0:
            self.y -= self.vy
            self.jumping = True
        if self.bounds[3] >= self.ground:
            self.vy = 0
            self.jumping = False
        else:
            self.vy -= 3
            if self.topB == False:
                self.y -= self.vy
            self.jumping = True


        for block in app.blocks:
            boundsA = self.getKirbyBounds(app)
            boundsB = block.getBlockBounds(app)
            
            if type(block) == badBlock:
                if block.touched == False:
                    block.touched = self.boundsIntersect(boundsA,boundsB)
                else:
                    self.nearbyEnemies.append(block.newE)
            elif type(block) == lifeBlock:
                if block.claimed == False:
                    block.claimed = self.boundsIntersect(boundsA,boundsB)
                if block.added == False and block.claimed == True:
                    self.lives += 1
                    block.added = True
            else:
                self.blockDistance(app,boundsA,boundsB)

    def boundsIntersect(self, boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
        (ax0, ay0, ax1, ay1) = boundsA
        (bx0, by0, bx1, by1) = boundsB
        if ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0)):
                return True
        else:
            return False

    def blockDistance(self, app, boundsA, boundsB):
        (ax0, ay0, ax1, ay1) = boundsA #kirb
        (bx0, by0, bx1, by1) = boundsB #block
        # print(f'{boundsA} bound A')
        # print(f'{boundsB} bound B')
      
        if ax0-bx1 < 15 and ax0-bx1 >= 0: 
            self.moveL = abs(bx1-ax0)
        elif (ax0 + self.moveL +5 >= bx0 and ax0 + self.moveL +5<= bx1) or ((ax0+ax1)/2 +self.moveL >=bx0 and (ax0+ax1)/2 +self.moveL <=bx1):
            if (ay0+ay1)/2>=by0 and (ay0+ay1)/2<=by0:
                self.canL = False
            else:
                self.canL = True
        if bx0-ax1 < 15 and bx0-ax1 >= 0: 
            self.moveR = abs(bx0-ax1)
        elif (ax1 + self.moveR +5 >= bx0 and ax1 + self.moveR +5 <= bx1) or ((ax0+ax1)/2 +self.moveR >=bx0 and (ax0+ax1)/2 +self.moveR <=bx1):
            if (ay0+ay1)/2>=by0 and (ay0+ay1)/2<=by0:
                self.canR = False
            else:
                self.canR = True
        if ay0-by1 < 15 and ay0-by1 >= 0 and (ax0+ax1)/2 >= bx0 and (ax0+ax1)/2 <= bx1: 
            self.up = abs(ay0-by1)
            
        elif ay0-self.vy <= by1 and ay0-self.vy >= by0 and (ax0+ax1)/2 >= bx0 and (ax0+ax1)/2 <= bx1:
            self.canJ = False

        if (ay1 >= by0 or ay1 >= by0-self.vy) and ((ax0+ax1)/2 >= bx0 and (ax0+ax1)/2<=bx1):
            if (ay0+ay1)/2 >= by0 and (ay0+ay1)/2 <= by1: 
                self.ground = by0
                self.vy = 0
                self.topB = True
        else:
            self.ground= app.height*0.8
            self.moveL = 15
            self.moveR = 15
            self.up = 15
        return(self.moveR,self.moveL,self.up)

    def makePlayerVisible(self,app):
    # scroll to make player visible as needed
        if (self.x < self.scrollX + self.scrollMargin):
            self.scrollX = self.x - self.scrollMargin
        if (self.x > self.scrollX + app.width - self.scrollMargin):
            self.scrollX = self.x - app.width + self.scrollMargin
        if self.x > app.width - self.scrollMargin:
            self.x = app.width - self.scrollMargin
        if self.x < self.scrollMargin:
            self.x = self.scrollMargin

    #from course website
    def movePlayer(self,app, dx):
        self.x += dx  
        self.makePlayerVisible(app)

    def loadAnimatedGif(self,path):
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

    

    def keyPressed(self, app, event):
        if (event.key == "Left"):
            if self.canL:
                self.movePlayer(app, -1*self.moveL)
                app.scrollX -= 5
            self.eating = False
            self.attacking = False
            self.state = 'L'
            # self.canL = True

        elif (event.key == "Right"):
            if self.canR:
                self.movePlayer(app, self.moveR)
                app.scrollX += 5
            self.eating = False
            self.attacking = False
            self.state = 'R'
            # self.canR = True
        elif (event.key == "Up"):
            self.jump()
            self.canJ = True
        elif (event.key == 'x'):
            self.eating = True   
        elif (event.key == 'z'):
            self.attacking = True
        elif (event.key == "Down"):
            self.slashing == True

    def drawLives(self,canvas, lives):
        cx,cy = self.x, self.y - 75
        for i in range(lives):
            canvas.create_rectangle(cx+20*i,cy,cx+20*(i+1),cy+20,fill = 'red')
        canvas.create_text(cx-10,cy+10,text = f'{self.getLives()} x', fill = 'black')

    def eat(self):
        for enemy in self.nearbyEnemies:
            if self.eating == True:
                if abs(enemy.getXpos() - self.getX()) < 100:
                    if type(enemy) != Boss:
                        enemy.lives -= 1
                    enemy.eaten = True
                if enemy.kind == 'metaknight.gif':
                    self.slashing = True
    
    def sword(self):
        for enemy in self.nearbyEnemies:
            if self.slashing == True:
                if abs(enemy.getXpos() - self.getX()) < 80:
                    enemy.lives -= 1
        self.slashing = False

    def punch(self,app):
        for enemy in self.nearbyEnemies:
            if self.attacking == True:
                if abs(enemy.getXpos() - self.getX()) < 40:
                    enemy.lives -= 1
        self.attacking == False

    def touched(self,app):
        if self.eating == False and self.attacking == False:
            for enemy in self.nearbyEnemies:
                intersected = self.boundsIntersect(self.getKirbyBounds(app),enemy.getEnemyBounds())
                if intersected == True and enemy.lives > 0:
                    enemy.lives -= 1
                    self.deductLife()

    def redrawAll(self,app, canvas):
        # if self.eating == True and self.slashing == True:
        #     spritePhotoImage = self.loadAnimatedGif(self.knight)
        if app.kirb.attacking == True:
            canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.fight))
            canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.fightL))
        elif app.kirb.eating == True and self.slashing == True:
            if self.state == 'R':
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.knightR))
            else:
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.knight))
        elif app.kirb.eating == True:
            if self.state == 'R':
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.suck))
            else:
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.suckL))
        elif app.kirb.jumping == True:
            if self.state == 'R':
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.float))
            else:
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.floatL))
        else:
            if self.state == 'R':
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.walk))
            else:
                canvas.create_image(app.kirb.x, app.kirb.y, image=ImageTk.PhotoImage(app.walkL))
        self.drawLives(canvas,self.lives)

    def getLives(self):
        return self.lives
        
    def deductLife(self):
        self.lives -= 1