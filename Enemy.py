from cmu_112_graphics import *
import random 

class Enemy:
    def __init__(self,kind,lives,x,y):
        self.lives = lives
        self.x = x
        self.y = y
        self.kind = kind
        self.spriteCounter = 0
        self.eaten = False

    def getXpos(self):
        return self.x

    def getYpos(self):
        return self.y

    def timerFired(self,app):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.loadAnimatedGif(self.kind))
        if self.kind == 'chilly.gif': 
            self.x -= 5
        elif self.kind == 'metaknight.gif':
            self.x += 10
            
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
            spritePhotoImage = self.loadAnimatedGif(self.kind)
            photoImage = spritePhotoImage[self.spriteCounter]
            canvas.create_image(self.x, self.y, image=photoImage)
        
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

    def timerFired(self,app):
        self.patrol(self)



