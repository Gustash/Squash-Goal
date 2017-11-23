#==============================================================================
# squash.py
# In-class program design demo
# k moves bat up, m moves bat down
#==============================================================================

from graphics import *
from rotation_test import *
from random import randint

import math

WALL_THICKNESS = 0.05
BAT_WIDTH = 0.15
BAT_X = 0.85
BAT_THICKNESS = 0.05
BALL_RADIUS = 0.03

def main():
    court = makeCourt()
    ball = makeBall(court)
    bat, lines = makeBat(court)
    playGame(court, ball, bat, lines)

def makeCourt():
    court = GraphWin("Squash", 500, 500)
    court.setCoords(0, 0, 1, 1)
    resetCourt(court)
    return court
    
def resetCourt(court):
    drawRectangle(court, Point(0, 0), Point(1, WALL_THICKNESS), "black")
    drawRectangle(court, Point(0, 1), Point(1, 1 - WALL_THICKNESS), "black")
    drawRectangle(court, Point(0, WALL_THICKNESS),
                  Point(WALL_THICKNESS, 1 - WALL_THICKNESS), "black")
    makeGoal(court)
    
def makeGoal(court):
    wall = randint(1, 3)
    if wall == 1: # Top wall
        pass
    elif wall == 2: # Left wall
        pass
    else: # Bottom wall
        pass
    
def playGame(court, ball, bat, lines):
    speedX = -0.00005
    speedY = 0.00004
    gameOver = False
    while not gameOver:
        speedX, speedY = checkBallHitWall(ball, speedX, speedY)
        speedX, speedY = checkBallHitBat(ball, bat, speedX, speedY, lines)
        ball.move(speedX, speedY)
        lines = checkMoveBat(court, bat, lines)
        gameOver = ball.getCenter().getX() > 1
        
def checkBallHitWall(ball, speedX, speedY):
    centre = ball.getCenter()
    if centre.getX() - BALL_RADIUS < WALL_THICKNESS:
        speedX = -speedX
    if centre.getY() + BALL_RADIUS >= 1 - WALL_THICKNESS or \
       centre.getY() - BALL_RADIUS <= WALL_THICKNESS:
        speedY = -speedY
    return speedX, speedY

def checkBallHitBat(ball, bat, speedX, speedY, lines):
    ballCentre = ball.getCenter()
    ballX = ballCentre.getX() + BALL_RADIUS
    ballY = ballCentre.getY()
    #topBat, botBat, rightBat, leftBat = getHighestAndLowestXAndY(bat.getPoints())
    
    for line in lines:
        collision = circleLineCollision(line.getP1(), line.getP2(), ball)
        if collision:
            direction = determineTerminalPoint(collision, ball)
            speedX = direction.getX()
            speedY = direction.getY()
    return speedX, speedY
    
def determineTerminalPoint(collision, ball):
    unit = 10000
    
    centre = ball.getCenter()
    vector = vsub(centre, collision)
    collisionX, collisionY = vector.getX(), vector.getY()
    vectorLength = math.sqrt(collisionX**2 + collisionY**2)
    u = Point((collisionX / vectorLength) / unit, (collisionY / vectorLength) / unit)
    return u
    
def getCollisionDirection(ball, collision):
    centre = ball.getCenter()
    line = Line(collision, centre)
    

def checkMoveBat(court, bat, lines):
    key = court.checkKey()
    if key != "":
        if key == "Up":
            bat.move(0, 0.01)
        elif key == "Down":
            bat.move(0, -0.01)
            
        if key == "Left":
            rotatePolygon(court, bat, 5)
        elif key == "Right":
            rotatePolygon(court, bat, -5)

        lines = getLines(bat)
    return lines
    
    
def makeBat(court):
    bat = drawPolygon(court, Point(BAT_X, 0.5 - BAT_WIDTH / 2),
                        Point(BAT_X + BAT_THICKNESS, 0.5 + BAT_WIDTH / 2),
                        "blue")
    lines = getLines(bat)
    return bat, lines

def makeBall(court):
    ball = Circle(Point(0.5, 0.5), BALL_RADIUS)
    ball.setFill("red")
    ball.setOutline("red")
    ball.draw(court) 
    return ball
    
def getHighestAndLowestXAndY(points):
    listOfY, listOfX = [], []
    for point in points:
        listOfX.append(point.getX())
        listOfY.append(point.getY())
    
    maxY = max(listOfY)
    minY = min(listOfY)
    maxX = max(listOfX)
    minX = min(listOfX)
    
    return maxY, minY, maxX, minX

def drawRectangle(win, point1, point2, colour):
    rectangle = Rectangle(point1, point2)
    rectangle.setFill(colour)
    rectangle.setOutline(colour)
    rectangle.draw(win)  
    return rectangle  
    
def drawPolygon(win, point1, point2, colour):
    top, bottom, right, left = getHighestAndLowestXAndY([point1, point2])
    top_left = Point(left, top)
    top_right = Point(right, top)
    bottom_right = Point(right, bottom)
    bottom_left = Point(left, bottom)
    
    polygon = Polygon(top_left, top_right, bottom_right, bottom_left)
    polygon.setFill(colour)
    polygon.setOutline(colour)
    polygon.draw(win)
    
    return polygon
    
main()

