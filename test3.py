"""
SUN HAO

"""
import pygame
from sys import exit
import numpy as np
    
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
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = [] 
knots = []
pos1 =[20,height-30]
pos2 =[width-20,height-30]
dis = 10
count = 0
myfont = pygame.font.Font(None, 30)
myfont2 = pygame.font.Font(None, 15)

#screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

# show "a" value
def FreeSystem(color='Blue', thick=3):
    pygame.draw.line(screen, color,pos1,pos2, thick)
    pygame.draw.circle(screen, color, pos1, thick)
    pygame.draw.circle(screen, color, pos2, thick)

def drawPoint(pt, color='GREEN', thick=3):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)

#HW2 implement drawLine with drawPoint
def drawLine(pt0, pt1, color='GREEN', thick=3):
    drawPoint((100,100), color,  thick)
    drawPoint(pt0, color, thick)
    drawPoint(pt1, color, thick)

def drawPolylines(color='GREEN', thick=3):
    if(count < 2): return
    for i in range(count-1):
        # drawLine(pts[i], pts[i+1], color)
        # pygame.draw.line(screen, color, pts[i], pts[i+1], thick)
        for j in range(dis):
            pox1 = pts[i][0]+(pts[i+1][0]-pts[i][0])/dis*j
            poy1 = (pts[i+1][1]-pts[i][1])/(pts[i+1][0]-pts[i][0])*(pox1-pts[i][0])+pts[i][1]
            poc1 = [pox1,poy1]
            pox2 = pts[i][0]+(pts[i+1][0]-pts[i][0])/dis*(j+1)
            poy2 = (pts[i+1][1]-pts[i][1])/(pts[i+1][0]-pts[i][0])*(pox2-pts[i][0])+pts[i][1]
            poc2 = [pox2,poy2]
            pygame.draw.line(screen, color,poc1,poc2, thick)

#Barycentric Coordinates
def BarycentricCoordinates(color=GREEN, thick=3):
    T1 = np.ones((3,3))
    
    for i in range(count):
        t=np.zeros((1,3))
        t[0,i]=1
        T1[0,i]= pts[i][0]
        T1[1,i]= pts[i][1]
        Ttext = str(t)
        #DrawText.BarycentricCoordinatesType(Ttext,color,screen,pts[i][0],pts[i][1])
        DrawText.BarycentricCoordinatesType("",color,screen,pts[i][0],pts[i][1])
    pygame.draw.circle(screen, color, pt, 5)
    DrawText.coordinateType(pt[0],pt[1],BLACK,screen,pt[0],pt[1],1)
    T2 = np.ones((3,1))
    T2[0,0] = pt[0]
    T2[1,0] = pt[1]
    Ttext = str(np.dot(np.linalg.inv(T1),T2).T.round(2))
    #DrawText.BarycentricCoordinatesType(Ttext,color,screen,pt[0],pt[1])
    DrawText.BarycentricCoordinatesType("",color,screen,pt[0],pt[1])

class DrawText:
    def NomarlType(text, font, color, surface, x, y):
        textobj = font.render(text, 2, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def TimeType(num,value,color, surface, x, y):
        textImage = myfont2.render("t"+str(num)+": "+str(value), True, color)
        surface.blit(textImage, (x-10, y+10))

    def TimeAniType(a,color, surface, x, y,Decimal=2):
        dec = (str)(Decimal)
        a1=format(a,'.'+ dec +'f')
        textImage = myfont.render('a='+a1, True, color)
        surface.blit(textImage, (x-20, y-50))

    def BarycentricCoordinatesType(text,color, surface, x, y):
        textImage = myfont2.render(text, True, color)
        surface.blit(textImage, (x-30, y-40))

    def coordinateType(xt,yt,color, surface,x,y,Decimal=1):
        dec = (str)(Decimal)
        xp = format(xt,'.'+ dec +'f')
        yp = format(yt,'.'+ dec +'f')
        #textImage = myfont2.render("("+xp+","+yp+")", True, color)
        textImage = myfont2.render("", True, color)
        surface.blit(textImage, (x-30, y-20))

def drawCurve(color=GREEN, thick=3):
    if  count==3:
        BarycentricCoordinates(color,thick)
        pygame.draw.line(screen, GREEN,pts[0],pts[count-1], 2)   
    
# the Animation of points' movement with text
def AnimationFunction(a,color='Red', thick=5):
    
    if  count==3:
        for i in range(count-1):
            DrawAniPoint(pts[i+1],pts[i],a,True)
        DrawAniPoint(pts[0],pts[count-1],a,True)
    else:
        for i in range(count-1):
            DrawAniPoint(pts[i],pts[i+1],a,True)  

def DrawAniPoint(P1,P2,a,show,line=False,color=RED, thick=5,max=1):
    x = P1[0]*(1-a)*max +P2[0]*a*max
    y = P1[1]*(1-a)*max +P2[1]*a*max
    pos = [x,y]
    drawPoint(pos, color, thick)
    if show:
        DrawText.coordinateType(x,y,color,screen,x,y,1)
#Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0
Aim = False
a=0
AimSpeed = 5

while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(60)
    time_passed_seconds = time_passed/10000.0
    screen.fill(WHITE)
    #FreeSystem()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        # play and stop Ain
        elif event.type == pygame.KEYDOWN:
            if Aim:
                Aim = False
            else:
                a=0
                Aim = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :
        pts.append(pt) 
        count += 1
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed)+" add pts ...")
    else:
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed))

    for i in range(count):
        pygame.draw.rect(screen, BLUE, (pts[i][0]-margin, pts[i][1]-margin, 2*margin, 2*margin), 5)

    if len(pts)>1:
        drawPolylines(GREEN, 2)
        # drawLagrangePolylines(BLUE, 10, 3)
        if len(pts)>2:
            drawCurve(BLUE,1)
    
    if Aim:
        AnimationFunction(a)
        a = a + time_passed_seconds*AimSpeed
        if a >= 1:
            a = 0
            Aim = False
    elif a!=0:
        AnimationFunction(a)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()

