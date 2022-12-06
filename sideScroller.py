from cmu_112_graphics import *
import random
import math

def appStarted(app):
    app.scrollX = 0 
    app.scrollMargin = 50
    app.playerX = app.scrollMargin
    app.playerY = 0
    app.playerWidth = 10
    app.playerHeight = 20
    app.walls = 5
    app.wallPoints = [0]*app.walls
    app.wallX = random.randint(100,200)
    app.wallY = random.randint(100,400)
    app.y0 = app.playerX
    app.wallWidth = random.randint(10,30)
    app.wallHeight = random.randint(10,50)
    app.wallSpacing = random.randint(50,100) # wall left edges are at 90, 180, 270,...
    app.currentWallHit = -1 # start out not hitting a wall
    app.touchedLeft = False
    app.touchedRight = False
    app.vy = 0
    app.stop = False
    app.moveR = 5
    app.moveL = 5
    app.up = 5
    app.ground = 0
    app.topB = False
    app.vx0 = 5
    app.vy0 = 50
    app.projectedX = []
    app.projectedY = []
    app.t = 0
    app.velocity = 0
    app.jumpForce = 7
    app.gravity = 9.81
    app.maxh = app.velocity ** 2 * math.sin(30) ** 2/(2*app.gravity)
    app.range = app.velocity ** 2 * math.sin(60) /app.gravity

# def updateX(app,t):
#     currentX = app.vx0 * t
#     app.projectedX.append(currentX)
#     return currentX

# def updateY(app,t):
#     currentY = app.y0 + app.vy0 * t - (4.9*t**2)
#     app.projectedY.append(currentY)
#     return currentY


# def timerFired(app):
    
    # if app.vy != 0:
    #     app.playerY += app.vy
    # if app.playerY == app.ground or app.playerY + app.vy < app.ground:
    #     app.vy = 0
    #     app.playerY = app.ground
    # else:
    #     app.vy -= 1
    #     if app.topB == False:
    #         app.playerY += app.vy
    #     for wall in range(app.walls):
    #         boundsA = getPlayerBounds(app)
    #         boundsB = getWallBounds(app,wall)
    #         wallDistance(app,boundsA,boundsB)


#     app.velocity = 0
#     app.velocity += app.gravity
#     app.playerY += app.velocity

def updateX(app,t):
    currentX = t
    app.projectedX.append(currentX)
    return currentX

def updateY(app,t):
    currentY = (-1*t)**2 + 4*t + 4
    app.projectedY.append(currentY)
    return currentY

def jump(app):
    app.playerY += 10

def timerFired(app):
    app.timerDelay = 500
    while app.playerY >= 0:
        newx = updateX(app,app.t+1)
        newy = updateY(app,app.t+1)
        print(newx)
        print(newy)
        app.playerX = newx
        app.playerY = newy
        app.t += 1


def getPlayerBounds(app):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = (app.playerX, app.height/2 - app.playerY)
    (x1, y0) = (x0 + app.playerWidth, y1 - app.playerHeight)
    return (x0, y0, x1, y1)

def getWallBounds(app, wall):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = ((1+wall) * app.wallSpacing, app.height/2-50)
    (x1, y0) = (x0 + app.wallWidth, y1 - app.wallHeight)
    return (x0, y0, x1, y1)

def getWallHit(app):
    # return wall that player is currently hitting
    # note: this should be optimized to only check the walls that are visible
    # or even just directly compute the wall without a loop
    playerBounds = getPlayerBounds(app)
    for wall in range(app.walls):
        wallBounds = getWallBounds(app, wall)
        if (boundsIntersect(app, playerBounds, wallBounds) == True):
            return wall
    return -1

def boundsIntersect(app, boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    if ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0)):
            return True
    
def wallDistance(app, boundsA, boundsB):
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    if abs(bx1-ax0) < 5  and ay1 >= by0 : app.moveL = abs(bx1-ax0)
    if abs(bx0-ax1) < 5 and ay1 >= by0: app.moveR = abs(bx0-ax1)
    if abs(by1-ay0) < 5 and (ax0+ax1)/2 >= bx0 and (ax0+ax1)/2 <= bx1: 
        app.up = abs(by1-ay0)
        app.vy -= 1
    if (ay1 + app.vy <= by0) and (ax0+ax1)/2 >= bx0 and (ax0+ax1)/2<=bx1:
        app.ground = by0
        app.vy = 0
        app.topB = True
    else:
        app.ground= 0

def checkForNewWallHit(app):
    # check if we are hitting a new wall for the first time
    wall = getWallHit(app)
    if (wall != app.currentWallHit):
        app.currentWallHit = wall
        if (wall >= 0):
            app.wallPoints[wall] += 1

def makePlayerVisible(app):
    # scroll to make player visible as needed
    if (app.playerX < app.scrollX + app.scrollMargin):
        app.scrollX = app.playerX - app.scrollMargin
    if (app.playerX > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.playerX - app.width + app.scrollMargin

def movePlayer(app, dx, dy):
    app.playerX += dx
    app.playerY += dy
    makePlayerVisible(app)
    checkForNewWallHit(app)

def sizeChanged(app):
    makePlayerVisible(app)

def mousePressed(app, event):
    app.playerX = event.x + app.scrollX
    checkForNewWallHit(app)

def keyPressed(app, event):
    if (event.key == "Left"):    
        movePlayer(app, -1*app.moveL, 0)
        app.moveL = 5
    elif (event.key == "Right"): 
        movePlayer(app, app.moveR, 0)
        app.moveR = 5
    elif (event.key == "Up"):    
        # app.jump = True
        jump(app)
        app.up = 5
    elif (event.key == "Down"):  movePlayer(app, 0, -5)

def redrawAll(app, canvas):
    # draw the base line
    lineY = app.height/2
    lineHeight = 5
    canvas.create_rectangle(0, lineY, app.width, lineY+lineHeight,fill="black")

    # draw the walls
    # (Note: should optimize to only consider walls that can be visible now!)
    sx = app.scrollX
    for wall in range(app.walls):
        (x0, y0, x1, y1) = getWallBounds(app, wall)
        fill = "orange" if (wall == app.currentWallHit) else "pink"
        canvas.create_rectangle(x0-sx, y0, x1-sx, y1, fill=fill)
        (cx, cy) = ((x0+x1)/2 - sx, (y0 + y1)/2)
        canvas.create_text(cx, cy, text=str(app.wallPoints[wall]), fill='black')
        cy = lineY + 5
        canvas.create_text(cx, cy, text=str(wall), anchor=N, fill='black')

    # draw the player
    (x0, y0, x1, y1) = getPlayerBounds(app)
    canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill="cyan")

    # draw the instructions
    msg = "Use arrows to move, hit walls to score"
    canvas.create_text(app.width/2, 20, text=msg, fill='black')

runApp(width=300, height=300)