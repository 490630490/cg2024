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

# the Animation of points' movement with text
def AnimationFunction(a,color='Red', thick=5):
    
    for i in range(count-1):
        x = pts[i][0]*(1-a) +pts[i+1][0]*a
        y = pts[i][1]*(1-a) +pts[i+1][1]*a
        pos = [x,y]
        drawPoint(pos, color, thick)
        xs =  format(x, '.1f')
        ys =  format(y, '.1f')
        textImage = myfont2.render("", True, color)
        screen.blit(textImage, (x-30, y-20))


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

