import pygame
import pygame.freetype
from pygame.sprite import Sprite
import numpy as np
from sys import exit

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'image/curve_pattern.png'
background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
Gary = (200, 200, 200)
lGary = (230, 230, 230)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pts = []
time = []
Trect = []
pos1 = [20, height - 30]
pos2 = [width - 20, height - 30]
dis = 30
count = 0
myfont = pygame.font.Font(None, 30)
myfont2 = pygame.font.Font(None, 15)
Menufont = pygame.font.Font(None, 15)
method = list()
method.append("Normal")
method.append("DrawLine with DrawPoint")
method.append("Barycentric coordinates")
method.append("Lagrange Interpolation")
method.append("Cubic Bezier")
method.append("Cubic Hermite")

CurrentModule = 5

# screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock = pygame.time.Clock()


# show "a" value
def FreeSystem(color=BLUE, thick=3):
    pygame.draw.line(screen, color, pos1, pos2, thick)
    pygame.draw.circle(screen, color, pos1, thick)
    pygame.draw.circle(screen, color, pos2, thick)
    if method[CurrentModule] == "Lagrange Interpolation":
        drawrect(pos1, RED, 0)
        DrawText.TimeType(0, 0, RED, screen, pos1[0], pos1[1])
        drawrect(pos2, RED, 0)
        DrawText.TimeType(len(time) - 1, time[count - 1], RED, screen, pos2[0], pos2[1])
        _DrawTime = DoingActive()
        _DrawTime.DrawInteractionRect(Trect, len(Trect), 1)
    elif method[CurrentModule] == "Cubic Bezier":
        pos = CubicBezierModule(pts,a,True)
        pygame.draw.circle(screen, RED , pos, 0)


class DrawText:
    def NomarlType(text, font, color, surface, x, y):
        textobj = font.render(text, 2, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def TimeType(num, value, color, surface, x, y):
        textImage = myfont2.render("t" + str(num) + ": " + str(value), True, color)
        surface.blit(textImage, (x - 10, y + 10))

    def TimeAniType(a, color, surface, x, y, Decimal=2):
        dec = (str)(Decimal)
        a1 = format(a, '.' + dec + 'f')
        textImage = myfont.render('a=' + a1, True, color)
        surface.blit(textImage, (x - 20, y - 50))

    def BarycentricCoordinatesType(text, color, surface, x, y):
        textImage = myfont2.render(text, True, color)
        surface.blit(textImage, (x - 30, y - 40))

    def coordinateType(xt, yt, color, surface, x, y, Decimal=1):
        dec = (str)(Decimal)
        xp = format(xt, '.' + dec + 'f')
        yp = format(yt, '.' + dec + 'f')
        textImage = myfont2.render("(" + xp + "," + yp + ")", True, color)
        surface.blit(textImage, (x - 30, y - 20))


def drawPoint(pt, color=GREEN, thick=3):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)


# HW2 implement drawLine with drawPoint
def drawLine(pt0, pt1, color=GREEN, thick=3):
    drawPoint((100, 100), color, thick)
    drawPoint(pt0, color, thick)
    drawPoint(pt1, color, thick)


def drawrect(pt, color=RED, pointFill=2):
    point = pygame.Rect(pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin)
    pygame.draw.rect(screen, color, point, pointFill)


class DoingActive:
    Rectmargin = 200

    def DrawInteractionRect(self, pointGroup, index, Mode=0):
        global checkPressedPoint
        for i in range(index):
            pointFill = 2

            if i + Mode * 100 == checkPressedPoint:
                self.Rectmargin = 200
            else:
                self.Rectmargin = margin

            drawrect(pointGroup[i], BLUE, pointFill)
            pointRange = pygame.Rect(pointGroup[i][0] - self.Rectmargin * 2, pointGroup[i][1] - self.Rectmargin * 2,
                                     2 * self.Rectmargin * 2, 2 * self.Rectmargin * 2)
            pointRangeDefend = pygame.Rect(pointGroup[i][0] - self.Rectmargin * 4,
                                           pointGroup[i][1] - self.Rectmargin * 4, 2 * self.Rectmargin * 4,
                                           2 * self.Rectmargin * 4)

            if Mode == 1:
                Ct = format(time[i + 1], '.2f')
                num = (str)(i + 1)
                DrawText.TimeType(num, Ct, RED, screen, pointGroup[i][0], pointGroup[i][1])

            if i + Mode * 100 == checkPressedPoint or checkPressedPoint == -1:
                if pointRangeDefend.collidepoint(pygame.mouse.get_pos()):
                    self.ButtonCheck = True
                    if pointRange.collidepoint(pygame.mouse.get_pos()):
                        pointFill = 0
                        drawrect(pointGroup[i], RED, pointFill)
                        if pressed1 == -1:
                            checkPressedPoint = i + Mode * 100
                            if Mode == 1:
                                pointGroup[i][0] = pygame.mouse.get_pos()[0]
                                if i > 0 and i < index - 1:
                                    if pointGroup[i][0] <= pointGroup[i - 1][0] + 5:
                                        pointGroup[i][0] = pointGroup[i - 1][0] + 5
                                    elif pointGroup[i][0] >= pointGroup[i + 1][0] - 5:
                                        pointGroup[i][0] = pointGroup[i + 1][0] - 5
                                elif i == 0 and i != index - 1:
                                    if pointGroup[i][0] <= pos1[0] + 5:
                                        pointGroup[i][0] = pos1[0] + 5
                                    elif pointGroup[i][0] >= pointGroup[i + 1][0] - 5:
                                        pointGroup[i][0] = pointGroup[i + 1][0] - 5
                                elif i == index - 1 and i != 0:
                                    if pointGroup[i][0] <= pointGroup[i - 1][0] + 5:
                                        pointGroup[i][0] = pointGroup[i - 1][0] + 5
                                    elif pointGroup[i][0] >= pos2[0] - 5:
                                        pointGroup[i][0] = pos2[0] - 5
                                else:
                                    if pointGroup[i][0] <= pos1[0] + 5:
                                        pointGroup[i][0] = pos1[0] + 5
                                    elif pointGroup[i][0] >= pos2[0] - 5:
                                        pointGroup[i][0] = pos2[0] - 5
                                time[i + 1] = ((pointGroup[i][0] - pos1[0]) / (pos2[0] - pos1[0])) * time[count - 1]
                            elif Mode == 2:
                                pointGroup[i] = pygame.mouse.get_pos()
                        else:
                            self.Rectmargin = margin
                            checkPressedPoint = -1
                else:
                    self.ButtonCheck = False


def drawPolylines(color=GREEN, thick=3):
    if (count < 2): return
    for i in range(count - 1):
        for j in range(dis):
            if method[CurrentModule] == "DrawLine with DrawPoint":
                pox1 = pts[i][0] + (pts[i + 1][0] - pts[i][0]) / dis * j
                if pts[i + 1][0] - pts[i][0] == 0:
                    poy1 = pts[i][1] + (pts[i + 1][1] - pts[i][1]) / dis * j
                else:
                    poy1 = (pts[i + 1][1] - pts[i][1]) / (pts[i + 1][0] - pts[i][0]) * (pox1 - pts[i][0]) + pts[i][1]
                poc1 = [pox1, poy1]
                drawPoint(poc1, color=GREEN, thick=1)
            else:
                pygame.draw.line(screen, color, pts[i], pts[i + 1], thick)


def drawCurve(color=GREEN, thick=3):
    if method[CurrentModule] == "Barycentric coordinates" and count == 3:
        BarycentricCoordinates(color, thick)
        pygame.draw.line(screen, GREEN, pts[0], pts[count - 1], 1)
    elif method[CurrentModule] == "Lagrange Interpolation":
        LagrangeInterpolation(color, thick)
    elif method[CurrentModule] == "Cubic Bezier":
        CubicBezier(color, thick)
    elif method[CurrentModule] == "Cubic Hermite":
        CubicHermite(color, thick)


def drawPopMenu(mouse_pos):
    global ButtonCheck
    width = 150
    height = 200
    point = pygame.Rect(mouse_pos[0], mouse_pos[1], width, height)
    pygame.draw.rect(screen, Gary, point, 0)
    if point.collidepoint(pygame.mouse.get_pos()):
        ButtonCheck = True
    else:
        ButtonCheck = False
    for i in range(len(method)):
        addItem(method[i], width, mouse_pos)


def addItem(Name="item", width=120, mouse_pos=[0.0, 0.0]):
    global CurrentModule
    global PopoutMenu
    global ButtonCheck
    global pressed1
    list = method.index(Name) * 31
    point = pygame.Rect(mouse_pos[0] + 5, mouse_pos[1] + 5 + list, width - 10, 30)

    if point.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, lGary, point, 0)
        if pressed1 == -1:
            CurrentModule = method.index(Name)
            PopoutMenu = False
            ButtonCheck = False
            pressed1 = 1
    else:
        pygame.draw.rect(screen, WHITE, point, 0)

    DrawText.NomarlType(Name, Menufont, BLACK, screen, mouse_pos[0] + 10, mouse_pos[1] + 15 + list)


# the Animation of points' movement with text
def AnimationFunction(a, color=RED, thick=5):
    # print(a)
    x = pos1[0] * (1 - a) + pos2[0] * a
    y = pos1[1] * (1 - a) + pos2[1] * a
    pos = [x, y]
    drawPoint(pos, color, thick)
    """ if method[CurrentModule] == "Lagrange Interpolation":
        DrawText.TimeAniType(a * (count - 1), color, screen, x, y, 2)
    else:
        DrawText.TimeAniType(a, color, screen, x, y, 2) """

    if method[CurrentModule] == "Barycentric coordinates" and count == 3:
        for i in range(count - 1):
            DrawAniPoint(pts[i + 1], pts[i], a, True)
        DrawAniPoint(pts[0], pts[count - 1], a, True)
    elif method[CurrentModule] == "Lagrange Interpolation":
        DrawAniLagrange(a)
    else:
        for i in range(count - 1):
            DrawAniPoint(pts[i], pts[i + 1], a, True)


def DrawAniPoint(P1, P2, a, show, line=False, color=RED, thick=5, max=1):
    x = P1[0] * (1 - a) * max + P2[0] * a * max
    y = P1[1] * (1 - a) * max + P2[1] * a * max
    pos = [x, y]
    drawPoint(pos, color, thick)
    """ if show:
        DrawText.coordinateType(x, y, color, screen, x, y, 1) """


def posWithTime(P1, P2, a):
    x = P1[0] * (1 - a) + P2[0] * a
    y = P1[1] * (1 - a) + P2[1] * a
    pos = [x, y]
    return pos


def DrawAniLagrange(a, color='Black', thick=1):
    T = a * (count - 1)
    showWorkingLine = []

    for k in range(count - 1):
        pos1 = LagrangeInterpolationModule(k + 1, k, 0)
        pos2 = LagrangeInterpolationModule(k + 1, k, count - 1)
        pygame.draw.line(screen, color, pos1, pos2, thick)
        if k == 0:
            continue
        for i in range(count - k):
            pos = LagrangeInterpolationModule(i + k, i, T)
            showWorkingLine.append(pos)

    for i in range(len(showWorkingLine) - 1):
        pygame.draw.line(screen, Gary, showWorkingLine[i], showWorkingLine[i + 1], thick)
        drawPoint(showWorkingLine[i + 1], BLUE, 2)

    drawPoint(showWorkingLine[0], BLUE, 2)
    pos = LagrangeInterpolationModule(count - 1, 0, T)
    drawPoint(pos, RED, 3)


# Barycentric Coordinates
def BarycentricCoordinates(color=GREEN, thick=3):
    T1 = np.ones((3, 3))

    for i in range(count):
        t = np.zeros((1, 3))
        t[0, i] = 1
        T1[0, i] = pts[i][0]
        T1[1, i] = pts[i][1]
        Ttext = str(t)
        DrawText.BarycentricCoordinatesType(Ttext, color, screen, pts[i][0], pts[i][1])
    pygame.draw.circle(screen, color, pt, 5)
    DrawText.coordinateType(pt[0], pt[1], BLACK, screen, pt[0], pt[1], 1)
    T2 = np.ones((3, 1))
    T2[0, 0] = pt[0]
    T2[1, 0] = pt[1]
    Ttext = str(np.dot(np.linalg.inv(T1), T2).T.round(2))
    DrawText.BarycentricCoordinatesType(Ttext, color, screen, pt[0], pt[1])


# Lagrange Interpolation
def LagrangeInterpolation(color=BLUE, thick=1):
    t = 0
    while t < count - 1:
        p1 = LagrangeInterpolationModule(count - 1, 0, t)
        p2 = LagrangeInterpolationModule(count - 1, 0, t + 0.1)
        pygame.draw.line(screen, color, p1, p2, thick)
        t += 0.1


def LagrangeInterpolationModule(MaxT, MinT, t):
    if MaxT - MinT > 1:
        q1 = LagrangeInterpolationModule(MaxT - 1, MinT, t)
        q2 = LagrangeInterpolationModule(MaxT, MinT + 1, t)
        result = np.dot(((time[MaxT] - t) / (time[MaxT] - time[MinT])), q1) + np.dot(
            ((t - time[MinT]) / (time[MaxT] - time[MinT])), q2)
        return result
    else:
        q1 = pts[MinT]
        q2 = pts[MaxT]
        result = np.dot((time[MaxT] - t) / (time[MaxT] - time[MinT]), q1) + np.dot(
            (t - time[MinT]) / (time[MaxT] - time[MinT]), q2)
        return result
    
def CubicBezier(color=BLUE, thick=1):
    t = 0
    l = 1/(count*10)
    while t < 1-l:
        firstpos = CubicBezierModule(pts,t,False)
        secondpos = CubicBezierModule(pts,t+l,False)
        pygame.draw.line(screen, color, firstpos, secondpos, thick)
        t+=l


def CubicBezierModule(poslist,t,draw=False):
    newposlist = []
    for i in  range(len(poslist)-1):
        pos = np.dot(poslist[i],(1-t))+np.dot(poslist[i+1],t)
        newposlist.append(pos)

    if(draw):
        pygame.draw.circle(screen, RED,newposlist[0], 5)
        for i in  range(len(newposlist)-1):
            pygame.draw.line(screen, BLACK, newposlist[i], newposlist[i+1], 1)
            pygame.draw.circle(screen, RED,newposlist[i+1], 5)
    
    if(len(newposlist)<=1):
        return newposlist[0]
    else:
        return CubicBezierModule(newposlist,t,draw)
        
def CubicHermite(color=BLUE, thick=1):
    l = 1/(count*10)
    for i in range(len(pts)-1):
        t = 0
        r1 = pts[i+1][1]-pts[i][1]
        if i==len(pts)-2 :
            r2 = pts[0][1]-pts[i+1][1]
        else:
            r2 = pts[i+2][1]-pts[i+1][1]
        while t < 1:
            firstpos = [(1-t)*pts[i][0]+t*pts[i+1][0],CubicHermiteModule(t,pts[i],pts[i+1],r1,r2)]
            secondpos = [(1-t-l)*pts[i][0]+(t+l)*pts[i+1][0],CubicHermiteModule(t+l,pts[i],pts[i+1],r1,r2)]
            pygame.draw.line(screen, color, firstpos, secondpos, thick)
            t+=l
    
def CubicHermiteModule(t,p1,p2,r1,r2):
    h00 = 2 * t**3 - 3 * t**2 + 1
    h01 = t**3 - 2 * t**2 + t
    h10 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    return h00 * p1[1] + h01 * r1 + h10 * p2[1] + h11 * r2





# Loop until the user clicks the close button.
done = False
PopoutMenu = False
ButtonCheck = False
MenuPos = [0, 0]
pressed1 = 0
pressed3 = 0
margin = 6
old_pressed1 = 0
old_pressed3 = 0
old_button1 = 0
old_button3 = 0
checkPressedPoint = -1
Aim = False
a = 0
AimSpeed = 5

while not done:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(40)
    time_passed_seconds = time_passed / 10000.0
    screen.fill(WHITE)
    FreeSystem()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pressed1 = -1
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pressed1 = 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pressed3 = -1
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            pressed3 = 1
        elif event.type == pygame.QUIT:
            done = True
        # play and stop Ain
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if Aim:
                Aim = False
            else:
                a = 0
                Aim = True
        elif event.type is pygame.QUIT:
            pygame.quit()

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed1 == -1 and pressed1 == 1 and old_button1 == 1 and button1 == 0 and checkPressedPoint == -1 and ButtonCheck == False:
        pts.append(pt)
        time.append(count)
        count += 1
        if len(time) >= 3:
            Trect.append(posWithTime(pos1, pos2, time[count - 2] / time[count - 1]))
            for i in range(len(Trect) - 1):
                Trect[i] = posWithTime(pos1, pos2, time[i + 1] / time[count - 1])
        # print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button1:"+repr(button1)+" pressed:"+repr(pressed1)+" add pts ...")
    elif old_pressed3 == -1 and pressed3 == 1 and old_button3 == 1 and button3 == 0 and checkPressedPoint == -1:
        if PopoutMenu:
            PopoutMenu = False
        else:
            PopoutMenu = True
            MenuPos = pt
    elif pressed1 == -1 and ButtonCheck == False:
        PopoutMenu = False
        # print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button3:"+repr(button3)+" pressed:"+repr(pressed3)+" PopoutMenu:"+repr(PopoutMenu))
    # else:
    # print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button1:"+repr(button1)+" pressed:"+repr(pressed1))

    if len(pts) > 1:
        drawPolylines(GREEN, 1)
        if len(pts) > 2:
            drawCurve(BLUE, 1)

        # drawLagrangePolylines(BLUE, 10, 3)

    for i in range(count):
        _Drawpiont = DoingActive()
        _Drawpiont.DrawInteractionRect(pts, count, 2)
        DrawText.coordinateType(pts[i][0], pts[i][1], BLACK, screen, pts[i][0], pts[i][1], 1)

    """ if PopoutMenu:
        drawPopMenu(MenuPos) """

    if Aim:
        AnimationFunction(a)
        a = a + time_passed_seconds * AimSpeed
        if a >= 1:
            a = 0
            Aim = False
    elif a != 0:
        AnimationFunction(a)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_button3 = button3
    old_pressed1 = pressed1
    old_pressed3 = pressed3

pygame.quit()

