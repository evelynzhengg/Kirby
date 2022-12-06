# def ct4(A):
#     for col in range(len(A[0]) - 1, -1, -1):
#         A[col] = sorted(A[col])
#         for row in range(len(A)):
#             if len(A[row][col]) >= 5:
#                 A[col][row] = "pat"
#             elif A[row][col].find("i") != -1:
#                 A[row][col] = "mike"
#     return A
# A = [["midterm", "fun"],
# ["positivity", "only"]]
# print(ct4(A))

# def isAscendingPower(n):
#     strNum = str(n)
#     digits = len(strNum)
#     total = 0
#     for digit in range(digits):
#         total += int(strNum[digit])**(digit+1)
#     if total == n:
#         return True
#     else:
#         return False

# def nthAscendingPowerNumber(n):
#     count = -1
#     guess = 1
#     while count != n:
#         if isAscendingPower(guess):
#             count += 1
#         guess += 1
#     return guess - 1

# assert(nthAscendingPowerNumber(0) == 1)
# assert(nthAscendingPowerNumber(1) == 2)
# assert(nthAscendingPowerNumber(9) == 89)
# assert(nthAscendingPowerNumber(12) == 518)
# assert(nthAscendingPowerNumber(16) == 2427)

def stockInfo(s):
    output = ''
    count = 0
    for part in s.splitlines():
        for sec in part.split('-'):
            count += 1
            if count == 2:
                output = output + sec + ":"
            else:
                for i in range(len(sec)):
                    if sec[i].isdigit() == False and sec[i] != '.':
                        break
                    if i == len(sec) -1:
                        output = output + sec + '\n'
        count = 0
    return output
s = '''09/14/07-AAPL-FC3d-E-47.50  \
06/05/12-GS-CH86-80.01\
11/12/03-BABA-110.53'''
print(stockInfo(s))
from cmu_112_graphics import *
import random

import copy
def ct3(a):
    b = copy.copy(a)
    c = copy.deepcopy(a)
    a[1] = "hack"
    b[0][1] = 20
    c[1][0] = a[1][1]
    c.append(b[0].pop(0))
    a.extend([a[0]])
    a[0][0]+=1
    print(f"a:{a}")
    print(f"b:{b}")
    print(f"c:{c}")
z = [ [ "cat", 4 ], [ "dog", 12 ] ]
ct3(z)
print(f"z:{z}")

L = [1,2]
L.append([3])
L.extend([3])
print(L.pop())


def containsAliases(L):
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            if L[i] is L[j]:
                return True
    return False
M = [1, 2]
L = [ [3, 4], [5, 6], M, [7, 8], M ] # contains aliases!
print(containsAliases(L)) # True

def digitCount(n):
    count = 0
    while n > 0:
        n//= 10
        count += 1
    return count

def isPresquareNumber(n):
    count = digitCount(n)
    for i in range(digitCount(n),0,-1):
        s = (n // (10**(count-1)))**2
        if  s == n%(10**(count-1)):
            return True
    return False
print(isPresquareNumber(11))
def nearestPreSquareNumber(n):
    diff = 0
    while True:
        if isPresquareNumber(n-diff):
            return n-diff
        elif isPresquareNumber(n+diff):
            return n+diff
        diff+=1
def testNearestPreSquareNumber():
    print('Testing nearestPreSquareNumber(n)...', end='')
    assert(nearestPreSquareNumber(0) == 11)
    assert(nearestPreSquareNumber(6000) == 6036)
    assert(nearestPreSquareNumber(-100) == 11)
 #Negatives should still work
    assert(nearestPreSquareNumber(20202) == 20004)
 #Halfway between 20004 and 20400
    assert(nearestPreSquareNumber(30100) == 30009)
 #Some solutions may be too slow!
    print('Passed!')
testNearestPreSquareNumber()

# def getRecord(team,scores):
#     wins = 0
#     losses = 0
#     ties = 0
#     home = False
#     found = False
#     hold = -1
#     other = -1
#     for line in scores.splitlines():
#         for game in line.split():
#             if game == team:
#                 home = True
#             if home == True and game.isdigit():
#                 hold = int(game)
#                 home == False
#             elif home == False and game.isdigit():
#                 other = int(game)
#             print(hold)
#             print(other)
#             if hold != -1 and other != -1:
#                 if hold > other:
#                     wins += 1
#                 elif hold < other:
#                     losses += 1
#                 else:
#                     ties +=1
#         hold = -1
#         other = -1
#     return (wins,losses,ties)

# scores = '''\
# Chi 2 - Pit 1
# Chi 2 - Pit 11
# Mia 13 - Pit 0
# Pit 4 - Mia 4
# Chi 2 - Mia 3'''
# print(getRecord('Pit', scores)) # == (1, 2, 1))
# assert(getRecord('Mia', scores) == (2, 0, 1))
# assert(getRecord('Chi', scores) == (1, 2, 0))
# assert(getRecord('Det', scores) == (0, 0, 0))
# print('Passed')
def distance(x0,x1,y0,y1):
    return ((x0-x1)**2+(y0-y1)**2)**0.5
def appStarted(app):
    app.r = 10
    app.blue = []
    app.change = 5
    
    
def redrawAll(app,canvas):
    canvas.create_oval(app.width/2-app.r,app.height/2-app.r,
    app.width/2+app.r,app.height/2+app.r,fill = 'red')
    drawDot(app,canvas)

def drawDot(app,canvas):
    for i in range(len(app.blue)):
        (x,y) = app.blue[i]
        if touched(app,x,y):
            continue
        else:
            canvas.create_oval(x-20,y-20,x+20,y+20,fill = 'blue')
        
def timerFired(app):
    timerDelay = 50
    app.r += app.change
    shrink(app)
def mousePressed(app,event):
    app.blue.append((event.x,event.y))
    print(app.blue)

def shrink(app):
    cx = app.width/2
    cy = app.height/2
    if cx + app.r >= app.width or cx - app.r <= 0:
        app.change = -5
    elif cy + app.r >= app.width or cy - app.r <= 0:
        app.change  = -5
    

def touched(app,x,y):
    if distance(x,app.width/2,y,app.height/2) <app.r + 20:
        return True
        
def keyPressed(app,event):
    if event.key: app.r = 0

runApp(width = 500, height = 500)
