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

SCREENSIZE = [800, 800]  # Size of our output display

lines = [] # A list containing lines

running = True

scale = 1

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

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_b:
                        print "Beams"

                        self.draw_thread()

                    elif event.key == pygame.K_d:
                        print "Dimensions"

                        self.dimension()

            for k in lines:
                k.draw(self.screen)

            pygame.display.update()
    
            pygame.event.clear()



    def draw_thread(self):

            draw = True

            while draw:

                self.screen.fill(white)

                for event in pygame.event.get():   

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_m:

                            self.main_thread()

                        elif event.key == pygame.K_d:

                            self.dimension()

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

                pygame.display.update()
    
                pygame.event.clear()


    def dimension(self):

        dimension = True

        while dimension:

            global scale

            print scale

            self.screen.fill(white)

            for event in pygame.event.get():   

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_m:

                        self.main_thread()

                    elif event.key == pygame.K_b:

                        self.draw_thread()

            for k in lines:
                k.draw(self.screen)

            for k in lines:
                k.rescale(self.screen)

            pygame.display.update()
    
            pygame.event.clear()

          



class Lines:

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

        #global scale


        #if self.input == 0:

            #scale = 1

        #else:

        #scale = self.input/self.length

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




if __name__ == '__main__':
    
    try:
        sim = Main()
        sim.main_thread()
        
    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()
