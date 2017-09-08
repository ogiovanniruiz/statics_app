import pygame

import matplotlib.lines as mlines

from pygame.locals import *

import numpy as np

import inputbox


red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]
ORANGE = (255, 102, 0)

SCREENSIZE = [800, 800]  # Size of our output display

lines = [] # A list containing lines

running = True

scale = 1

supportRun = True

fixed_supports = []
pinned_supports = []
roller_supports = []

#support_type = "none"

#z = 0

clock = pygame.time.Clock()

class Main:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.screen.fill(white)
        pygame.display.set_caption("Draw Lines and Shit")

        self.myfont = pygame.font.SysFont("arial", 15)

        self.P1 = [0,0] # Place to store starting point of a line

        self.P2 = [0,0] # Place to store ending point of a line

        self.flag = False #Flag used to check mouse condition while dragging lines


    def main_thread(self):

        while(running):
             
            self.screen.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check if close button has been pressed
                        pygame.quit() #quits pygame
                        quit() #quits   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        print "Beams"
                        self.draw_thread()
                    elif event.key == pygame.K_d:
                        print "Dimensions"
                        self.dimension()
                    elif event.key == pygame.K_s:
                        print "Supports"
                        self.support(self.screen)

            for k in lines:
                k.draw(self.screen)

            for i in fixed_supports:
                    i.draw_support(self.screen)

            for i in pinned_supports:
                i.draw_support(self.screen)

            for i in roller_supports:
                i.draw_support(self.screen)

            pygame.display.update()
    
            pygame.event.clear()

    def draw_thread(self):

            draw = True

            while draw:

                self.screen.fill(white)

                for event in pygame.event.get():   
                    if event.type == pygame.QUIT: #check if close button has been pressed
                        pygame.quit() #quits pygame
                        quit() #quits
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            draw = False
                            print "Main"
                            self.main_thread()
                        elif event.key == pygame.K_d:
                            print "Dimensions"
                            self.dimension()
                        elif event.key == pygame.K_s:
                            print "Supports"
                            self.support(self.screen)

                if (pygame.mouse.get_pressed()[0]) and (self.flag == False):
                    self.P1[:] = pygame.mouse.get_pos()
                    self.flag = True
                elif (pygame.mouse.get_pressed()[0]) and (self.flag == True):
                    self.P2[:] = pygame.mouse.get_pos()
                    if (-10 < (self.P2[0] - self.P1[0]) < 10) :
                        self.P2[0] = self.P1[0]
                    if (-10 < (self.P2[1] - self.P1[1]) < 10) :
                        self.P2[1] = self.P1[1]

                    pygame.draw.line(self.screen, red, self.P1[:],  self.P2[:], 3)
                    pygame.draw.circle(self.screen, red, [int(self.P1[0]), int(self.P1[1])], 5, 5)
                    pygame.draw.circle(self.screen, red, [int(self.P2[0]), int(self.P2[1])], 5, 5)
                    length = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))
                    dim = scale*length
                    temp_length = self.myfont.render(str("%.1f" % dim), 1, red)

                    self.screen.blit(temp_length, self.P1[:])

                elif (pygame.mouse.get_pressed()[0] == False) and (self.flag == True):
                    self.P2[:] = pygame.mouse.get_pos() 
                    if (-10 < (self.P2[0] - self.P1[0]) < 10) :
                        self.P2[0] = self.P1[0]
                    if (-10 < (self.P2[1] - self.P1[1]) < 10) :
                        self.P2[1] = self.P1[1]

                    lines.append(Lines(self.P1[:], self.P2[:], black))

                    self.flag = False

                for k in lines:
                    k.draw(self.screen)

                for i in fixed_supports:
                    i.draw_support(self.screen)

                for i in pinned_supports:
                    i.draw_support(self.screen)

                for i in roller_supports:
                    i.draw_support(self.screen)

                pygame.display.update()
    
                pygame.event.clear()


    def support(self, screen):

        display = screen

        support_type = "none"

        z=0
        
        while supportRun:

            display.fill(white)

            x,y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check if close button has been pressed
                    pygame.quit() #quits pygame
                    quit() #quits
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        print "Beams"
                        self.draw_thread()
                    elif event.key == pygame.K_d:
                        print "Dimensions"
                        self.dimension()

                    if event.key == pygame.K_f:
                        print("fixed selected")
                        support_type = "fixed"
                    if event.key == pygame.K_p:
                        print("pinned selected")
                        support_type = "pinned"
                    if event.key == pygame.K_r:
                        print("roller selected")
                        support_type = "roller"
                    if event.key == pygame.K_BACKSPACE:
                        print("delete selected")
                        support_type = "delete"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    z = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    z = 0

            if support_type == "fixed":
                pygame.draw.rect(display, red, [x, y, 30, 15])
            if z == 1 and support_type == "fixed":
                fixed_supports.append(Support(y, x, red, support_type, 30, 15))
                z = 5

            if support_type == "pinned":
                pygame.draw.polygon(display, blue, ((x,y),(x-15,y+20), (x+15,y+20)))
            if z == 1 and support_type == "pinned":
                pinned_supports.append(Support(y, x, blue, support_type))
                z = 4

            if support_type == "roller":
                pygame.draw.polygon(display, black, ((x,y),(x-15,y+20), (x+15,y+20)))
                pygame.draw.circle(display, black, (x, y+25), 5)
                pygame.draw.circle(display, black, (x+10, y+25), 5)
                pygame.draw.circle(display, black, (x-10, y+25), 5)
            if z == 1 and support_type == "roller":
                roller_supports.append(Support(y, x, black, support_type))
                z = 4

            elif z > 1:
                z -= 1

            for k in lines:
                k.draw(self.screen)

            for i in fixed_supports:
                i.draw_support(display)

            for i in pinned_supports:
                i.draw_support(display)

            for i in roller_supports:
                i.draw_support(display)

            if support_type == "delete":
                for i in fixed_supports:
                    i.check(display, z)

            if support_type == "delete":
                for i in pinned_supports:
                    i.check(display, z)

            if support_type == "delete":
                for i in roller_supports:
                    i.check(display, z)

            clock.tick(60)

            pygame.display.update()

    def dimension(self):

        dimension = True

        while dimension:

            global scale

            #print scale

            self.screen.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check if close button has been pressed
                        pygame.quit() #quits pygame
                        quit() #quits   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        print "Main"
                        dimension = False
                        self.main_thread()
                    elif event.key == pygame.K_b:
                        dimension = False
                        print "Beams"
                        self.draw_thread()
                    elif event.key == pygame.K_s:
                        dimension = False
                        print "Supports"
                        self.support(self.screen)

            for k in lines:
                k.draw(self.screen)

            for k in lines:
                k.rescale(self.screen)

            for i in fixed_supports:
                    i.draw_support(self.screen)

            for i in pinned_supports:
                i.draw_support(self.screen)

            for i in roller_supports:
                i.draw_support(self.screen)

            pygame.display.update()
    
            pygame.event.clear()

class Lines():

    p1 = 0
    p2 = 0
    color = [0,0,0]

    def __init__(self,p1,p2, color):

        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.myfont = pygame.font.SysFont("arial", 15)

        self.flag_A = False
        self.flag_B = False
        self.flag_C = False

        self.input = 0

    def draw(self,screen):

        self.length = np.linalg.norm(np.array(self.p1) - np.array(self.p2))

        self.dim = scale*self.length

        pygame.draw.line(screen, self.color, self.p1,  self.p2, 3)
        pygame.draw.circle(screen, self.color, [int(self.p1[0]), int(self.p1[1])], 5, 5)
        pygame.draw.circle(screen, self.color, [int(self.p2[0]), int(self.p2[1])], 5, 5)

        final_length = self.myfont.render(str("%.1f" % self.dim), 1, black)

        screen.blit(final_length, self.p1)

    def rescale(self,screen):

        mouse = pygame.mouse.get_pos()

        dist_A = np.linalg.norm(mouse - np.array(self.p1))

        dist_B = np.linalg.norm(mouse - np.array(self.p2))

        if (round(dist_A + dist_B) == round(self.length)) or ((dist_A < 6) or (dist_B < 6)):
            pygame.draw.line(screen, red, (self.p1), (self.p2), 3)
            pygame.draw.circle(screen, red, [int(self.p1[0]), int(self.p1[1])], 5, 5)
            pygame.draw.circle(screen, red, [int(self.p2[0]), int(self.p2[1])], 5, 5)

            if (dist_A < 6) and (pygame.mouse.get_pressed()[0]):
                self.flag_A = True
            elif (dist_B < 6) and (pygame.mouse.get_pressed()[0]):
                self.flag_B = True
            elif (round(dist_A + dist_B) == round(self.length)) and (pygame.mouse.get_pressed()[0]):
                self.flag_C = True
            elif (pygame.mouse.get_pressed()[0]) == False:
                self.flag_A = False
                self.flag_B = False

        if self.flag_A:
            self.p1 = mouse
        elif self.flag_B:
            self.p2 = mouse
        elif self.flag_C:
            try:
                self.input = int(inputbox.ask(screen, 'Scale to'))

                global scale
                scale = self.input/self.length
                self.flag_C = False

            except ValueError:
                print "Not a number"

class Support():

    def __init__(self, y, x, color, support, width=0, height=0):
        
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.color = color
        self.support = support
        self.mouse = pygame.mouse.get_pos()
        
    def draw_support(self, screen):

        display = screen

        if self.support == "fixed":
            pygame.draw.rect(display, self.color, [self.x, self.y, self.width, self.height])
        if self.support == "pinned":
            pygame.draw.polygon(display, self.color, 
                                ((self.x,self.y),(self.x-15,self.y+20), 
                                (self.x+15,self.y+20)))
        if self.support == "roller":
            pygame.draw.polygon(display, self.color, 
                                ((self.x,self.y),(self.x-15,self.y+20), 
                                (self.x+15,self.y+20)))
            pygame.draw.circle(display, self.color, (self.x, self.y+25), 5)
            pygame.draw.circle(display, self.color, (self.x+10, self.y+25), 5)
            pygame.draw.circle(display, self.color, (self.x-10, self.y+25), 5)

    def check(self, screen, click=0):

        display = screen

        mX,mY = pygame.mouse.get_pos()

        if (self.x <= mX <= self.x+30) and (self.y <= mY <= self.y+15) and self.support == "fixed":
            pygame.draw.rect(display, ORANGE, [self.x, self.y, 30, 15])
        if (self.x <= mX <= self.x+30) and (self.y <= mY <= self.y+15) and self.support == "fixed" and click == 1:
            fixed_supports.remove(self)


        if (self.x-15 <= mX <= self.x+30) and (self.y <= mY <= self.y+20) and self.support == "pinned":
            pygame.draw.polygon(display, ORANGE, 
                                ((self.x,self.y),(self.x-15,self.y+20), 
                                (self.x+15,self.y+20)))
        if (self.x-15 <= mX <= self.x+30) and (self.y <= mY <= self.y+20) and self.support == "pinned" and click == 1:
            pinned_supports.remove(self)


        if (self.x-15 <= mX <= self.x+30) and (self.y <= mY <= self.y+30) and self.support == "roller":
            pygame.draw.polygon(display, ORANGE, 
                                ((self.x,self.y),(self.x-15,self.y+20), 
                                (self.x+15,self.y+20)))
            pygame.draw.circle(display, ORANGE, (self.x, self.y+25), 5)
            pygame.draw.circle(display, ORANGE, (self.x+10, self.y+25), 5)
            pygame.draw.circle(display, ORANGE, (self.x-10, self.y+25), 5)
        if (self.x-15 <= mX <= self.x+30) and (self.y <= mY <= self.y+30) and self.support == "roller" and click == 1:
            roller_supports.remove(self)

if __name__ == '__main__':
    
    try:
        sim = Main()
        sim.main_thread()
        
    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()
