from graphics import *
import math

def rotatePolygon(win, polygon, angle):
    centrePoint = getCentreOfPolygon(polygon)
    rotatedPoints = []
    for point in polygon.getPoints():
        rotatedPoints.append(rotatePoint(centrePoint, point, angle))
    polygon.points = rotatedPoints
    polygon.undraw()
    polygon.draw(win)
    return polygon
    
def getCentreOfPolygon(polygon):
    # Only tested with rectangles
    listOfX = []
    listOfY = []
    for point in polygon.getPoints():
        listOfX.append(point.getX())
        listOfY.append(point.getY())
    middleX = (max(listOfX) + min(listOfX)) / 2
    middleY = (max(listOfY) + min(listOfY)) / 2
    return Point(middleX, middleY)    
    
def rotatePoint(centrePoint,point,angle):
    """Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    pointX, centrePointX = point.getX(), centrePoint.getX()
    pointY, centrePointY = point.getY(), centrePoint.getY()
    
    angle = math.radians(angle)
    tempPoint = Point(pointX - centrePointX, pointY - centrePointY)
    tempPointX, tempPointY = tempPoint.getX(), tempPoint.getY()
    tempPoint = Point(tempPointX * math.cos(angle) - tempPointY * math.sin(angle), tempPointX * math.sin(angle) + tempPointY * math.cos(angle))
    tempPointX, tempPointY = tempPoint.getX(), tempPoint.getY()
    tempPoint = Point(tempPointX + centrePointX , tempPointY + centrePointY)
    return tempPoint
    
def getLines(polygon):
    lines = []
    for i in range(-1, len(polygon.getPoints()) - 1):
        p1 = polygon.getPoints()[i]
        p2 = polygon.getPoints()[i + 1]
        line = Line(p1, p2)
        lines.append(line)
    
    return lines

def is_between(a,c,b):
    return distanceBetweenPoints(a,c) + distanceBetweenPoints(c,b) == distanceBetweenPoints(a,b)
    
def distanceBetweenPoints(p1, p2):
    width = p1.getX() - p2.getX()
    height = p1.getY() - p2.getY()
    return (width**2 + height**2)**0.5
    
def vsub(a,b):
    ax, ay = a.getX(), a.getY()
    bx, by = b.getX(), b.getY()
    return Point(ax - bx, ay - by)
    
def circleLineCollision(p1, p2, circle):
    centre = circle.getCenter()
    radius = circle.getRadius()
    
    localP1 = vsub(p1, centre)
    localP2 = vsub(p2, centre)
    p2MinusP1 = vsub(p2, p1)
    
    a = p2MinusP1.getX()**2 + p2MinusP1.getY()**2
    b = 2 * ((p2MinusP1.getX() * localP1.getX()) + (p2MinusP1.getY() * localP1.getY()))
    c = localP1.getX()**2 + localP1.getY()**2 - radius**2
    delta =  b**2 - (4 * a * c)
    if delta < 0:
        # No collision
        return None
    elif delta == 0:
        # Only one point collision
        u = -b / (2 * a)
        collisionPoint = Point(p1.getX() + (u * p2MinusP1.getX()), p1.getY() + (u * p2MinusP1.getY()))
        if is_between(p1, collisionPoint, p2):
            return collisionPoint
    elif delta > 0:
        # Collided with more than one point
        sqrtDelta = math.sqrt(delta)
        
        u1 = (-b + sqrtDelta) / (2 * a)
        u2 = (-b - sqrtDelta) / (2 * a)
        
        collisionPoint1 = Point(p1.getX() + (u1 * p2MinusP1.getX()), p1.getY() + (u1 * p2MinusP1.getY()))
        collisionPoint2 = Point(p1.getX() + (u2 * p2MinusP1.getX()), p1.getY() + (u2 * p2MinusP1.getY()))

        if distanceBetweenPoints(centre, collisionPoint1) < distanceBetweenPoints(centre, collisionPoint2) and is_between(p1, collisionPoint1, p2):
            return collisionPoint1
        elif is_between(p1, collisionPoint2, p2):
                return collisionPoint2
            
    
def test_logic():
    win = GraphWin()
    win.setCoords(0, 0, 200, 200)
    
    polygonP1 = Point(100, 100)
    polygonP2 = Point(40, 100)
    polygonP3 = Point(40, 50)
    polygonP4 = Point(100, 50)
    
    centrePoint = Point(70, 75)
    
    polygon = Polygon(polygonP1, polygonP2, polygonP3, polygonP4)
    polygon.draw(win)
    
    polygon = rotatePolygon(win, polygon, 90)
    
    circle = Circle(Point(35, 45), 20)
    circle.draw(win)
    
    lines = getLines(polygon)
    for line in lines:
        collisions = circleLineCollision(line.getP1(), line.getP2(), circle)
        if collisions:
            for collision in collisions:
                print(is_between(line.getP1(), collision, line.getP2()))