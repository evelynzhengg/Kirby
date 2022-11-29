from cmu_112_graphics import *
import math
class Kirby:
    def __init__(self,action,lives,x,y):
        self.action = action
        self.lives = lives
        self.x = x
        self.y = y
        self.float = 'kirbyfloat.gif'
        self.walk = 'kirby-walk.gif'
        self.suck = 'kirbyInhale.gif'
        self.fight = 'kirbyfight.gif'
        self.knight = 'kirbyknight.gif'
        self.spriteCounter = 0
        self.jumping = False
        self.eating = False
        self.attacking = False
        self.slashing = True
        self.spritePhotoImage = self.walk
        self.nearbyEnemies = []
        self.scrollX = 0
        self.scrollMargin = 20
        self.vy = 0
        self.moveR = 15
        self.moveL = 15
        self.up = 20
        self.ground = 600
        self.topB = False
        

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getKirbyBounds(self):
        (x0,y0) = (self.x - 50, self.y - 50)
        (x1,y1) = (self.x + 50, self.y + 50)
        return (x0,y0,x1,y1)

    def jump(self):
        self.jumping = True
        self.vy += self.up 

    def timerFired(self,app):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.kirbState())
        self.eat()
        self.touched()
        self.punch()
        self.sword()
        if self.vy != 0:
            self.y -= self.vy
            self.jumping = True
        if self.y >= self.ground:
            self.vy = 0
            self.y = self.ground 
            print('come in')
            self.jumping = False
        else:
            self.vy -= 3
            if self.topB == False:
                self.y -= self.vy
            self.jumping = True
        for block in app.normBlocks:
            print('timer fired')
            boundsA = self.getKirbyBounds()
            boundsB = block.getBlockBounds()
            self.blockDistance(app,boundsA,boundsB)

    def blockDistance(self, app, boundsA, boundsB):
        (ax0, ay0, ax1, ay1) = boundsA #kirb
        (bx0, by0, bx1, by1) = boundsB #block
        print(boundsA)
        print(boundsB)
        if abs(bx1-ax0) < 15  and (ay1+ay0)/2 >= by0 and (ay1+ay0)/2 <= by1 : 
            self.moveL = abs(bx1-ax0)
            print('left')
        if abs(bx0-ax1) < 15 and (ay1+ay0)/2 >= by0 and (ay1+ay0)/2 <= by1: 
            self.moveR = abs(bx0-ax1)
            print('right')
        if abs(ay0-by1) < 20: 
            self.up = abs(ay0-by1)
            print('up')
            self.vy = 0
        if (ay1 <= by0 and ay1 >= by0-self.vy) and (ax0 >= bx0 and ax1<=bx1):
            self.ground = by0
            self.vy = 0
            self.topB = True
        else:
            self.ground= 550

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
    def movePlayer(self,app, dx, dy):
        self.x += dx  
        self.y -= dy
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
            self.movePlayer(app, -1*self.moveL, 0)
            self.eating = False
            self.attacking = False
        elif (event.key == "Right"): 
            self.movePlayer(app, self.moveR, 0)
            self.eating = False
            self.attacking = False
        elif (event.key == "Up"):
            self.jump()
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
                    enemy.lives = 0
                    enemy.eaten = True
            if enemy.kind == 'metaknight.gif':
                self.slashing = True
    
    def sword(self):
        for enemy in self.nearbyEnemies:
            if self.slashing == True:
                if abs(enemy.getXpos() - self.getX()) < 80:
                    enemy.lives -= 1
        self.slashing = False

    def punch(self):
        for enemy in self.nearbyEnemies:
            if self.attacking == True:
                if abs(enemy.getXpos() - self.getX()) < 40:
                    enemy.lives -= 1
        self.attacking == False

    def touched(self):
        if self.eating == False and self.attacking == False:
            for i in range(len(self.nearbyEnemies)):
                if abs(self.nearbyEnemies[i].getXpos() - self.getX()) <= 20 and self.nearbyEnemies[i].lives > 0:
                    if abs(self.nearbyEnemies[i].getYpos() - self.getY()) <= 60:
                        self.nearbyEnemies[i].lives = 0
                        self.deductLife()
                
    def kirbState(self):
        spritePhotoImage = ''
        if self.eating == True and self.slashing == True:
            spritePhotoImage = self.loadAnimatedGif(self.knight)
        elif self.attacking == True:
            spritePhotoImage = self.loadAnimatedGif(self.fight)
        elif self.eating == True:
            spritePhotoImage = self.loadAnimatedGif(self.suck)
        # elif self.jumping == True:
        #     spritePhotoImage = self.loadAnimatedGif(self.float)
        else:
            spritePhotoImage = self.loadAnimatedGif(self.walk)
        return spritePhotoImage

    def redrawAll(self,app, canvas):
        if self.eating == True and self.slashing == True:
            spritePhotoImage = self.loadAnimatedGif(self.knight)
        elif self.attacking == True:
            spritePhotoImage = self.loadAnimatedGif(self.fight)
        elif self.eating == True:
            spritePhotoImage = self.loadAnimatedGif(self.suck)
        # elif self.jumping == True:
        #     spritePhotoImage = self.loadAnimatedGif(self.float)
        else:
            spritePhotoImage = self.loadAnimatedGif(self.walk)
        photoImage = spritePhotoImage[app.spriteCounter]
        canvas.create_image(self.x, self.y, image=photoImage)
        self.drawLives(canvas,self.lives)

    def getLives(self):
        return self.lives
        
    def deductLife(self):
        self.lives -= 1