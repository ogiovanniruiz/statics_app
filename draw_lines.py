import pygame

import numpy as np

import inputbox

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]
ORANGE = (255, 102, 0)

SCREENSIZE = [800, 800]  # Size of our output display

mode_pos = [100, 100]

beams = []  # A list containing lines

forces = []  # A List containing force vectors

scale = 1

scale_forces = 1

supportRun = True

fixed_supports = []
pinned_supports = []
roller_supports = []

clock = pygame.time.Clock()

# ======================================================================================================================
# The Screen Class sets up the pygame environment


class Screen:
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(SCREENSIZE)

        pygame.display.set_caption("Static App")

        self.font = pygame.font.SysFont("arial", 15)

    def pane(self, mode):

        self.screen.fill(white)

        temp_length = self.font.render(str(mode), 1, red)

        self.screen.blit(temp_length, mode_pos)

        return self.screen

# ======================================================================================================================


class Drawings:
    def __init__(self):

        self.color = [0, 0, 0]

        self.P1 = [0, 0]

        self.P2 = [0, 0]

        self.flag = False

    def temporary_draw(self, screen, font, mode):

        if (pygame.mouse.get_pressed()[0]) and (not self.flag):

            self.P1[:] = pygame.mouse.get_pos()

            self.flag = True

        elif (pygame.mouse.get_pressed()[0]) and self.flag:

            self.P2[:] = pygame.mouse.get_pos()

            if -10 < (self.P2[0] - self.P1[0]) < 10:

                self.P2[0] = self.P1[0]

            if -10 < (self.P2[1] - self.P1[1]) < 10:

                self.P2[1] = self.P1[1]

            if mode == "Beams":

                self.color = red

            elif mode == "Forces":

                self.color = green

            pygame.draw.line(screen, self.color, self.P1[:], self.P2[:], 3)

            pygame.draw.circle(screen, self.color, [int(self.P1[0]), int(self.P1[1])], 5, 5)

            pygame.draw.circle(screen, self.color, [int(self.P2[0]), int(self.P2[1])], 5, 5)

            length = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))

            dim = scale * length

            temp_length = font.render(str("%.1f" % dim), 1, self.color)

            screen.blit(temp_length, self.P1[:])

        elif (not pygame.mouse.get_pressed()[0]) and self.flag:

            self.P2[:] = pygame.mouse.get_pos()

            if -10 < (self.P2[0] - self.P1[0]) < 10:

                self.P2[0] = self.P1[0]

            if -10 < (self.P2[1] - self.P1[1]) < 10:

                self.P2[1] = self.P1[1]

            if mode == "Beams":

                beams.append(Beams(self.P1[:], self.P2[:], black))

            elif mode == "Forces":

                forces.append(Forces(self.P1[:], self.P2[:], blue))

            self.flag = False

    def permanent_draw(self, screen, font):

        for k in beams:
            k.permanent_draw(screen, font)

        for k in forces:
            k.permanent_draw(screen, font)

    def rescale(self, screen, mode):

        for k in beams:
            k.rescale(screen, mode)

        for k in forces:
            k.rescale(screen, mode)

# ======================================================================================================================
# The supports Class

# ======================================================================================================================
# The Lines Class contains parameters


class Lines:

    point_a = [0, 0]
    point_b = [0, 0]
    color = [0, 0, 0]

    def __init__(self, point_a, point_b, color):

        self.point_a = point_a

        self.point_b = point_b

        self.color = color

        self.flag_A = False

        self.flag_B = False

        self.flag_C = False

        self.flag_D = False

        self.flag_E = False

    def permanent_draw(self, screen, font):

        length = np.linalg.norm(np.array(self.point_a) - np.array(self.point_b))

        dim = scale*length

        pygame.draw.line(screen, self.color, self.point_a,  self.point_b, 3)

        pygame.draw.circle(screen, self.color, [int(self.point_a[0]), int(self.point_a[1])], 5, 5)

        pygame.draw.circle(screen, self.color, [int(self.point_b[0]), int(self.point_b[1])], 5, 5)

        final_length = font.render(str("%.1f" % dim), 1, black)

        screen.blit(final_length, self.point_a)

    def rescale(self, screen, mode):

        mouse = pygame.mouse.get_pos()

        dist_a = np.linalg.norm(mouse - np.array(self.point_a))

        dist_b = np.linalg.norm(mouse - np.array(self.point_b))

        length = np.linalg.norm(np.array(self.point_a) - np.array(self.point_b))

        dim = scale * length

        if (round(dist_a + dist_b) == round(length)) or ((dist_a < 6) or (dist_b < 6)):

            pygame.draw.line(screen, red, self.point_a, self.point_b, 3)

            pygame.draw.circle(screen, red, [int(self.point_a[0]), int(self.point_a[1])], 5, 5)

            pygame.draw.circle(screen, red, [int(self.point_b[0]), int(self.point_b[1])], 5, 5)

            if (dist_a < 6) and (pygame.mouse.get_pressed()[0]):

                self.flag_A = True

            elif (dist_b < 6) and (pygame.mouse.get_pressed()[0]):

                self.flag_B = True

            elif (round(dist_a + dist_b) == round(length)) and (pygame.mouse.get_pressed()[0]):

                self.flag_C = True

            elif (dist_a < 6) and (pygame.mouse.get_pressed()[2]):

                self.flag_D = True

            elif (dist_b < 6) and (pygame.mouse.get_pressed()[2]):

                self.flag_E = True

            elif (pygame.mouse.get_pressed()[0]) == False:

                self.flag_A = False
                self.flag_B = False

        if self.flag_A:

            self.point_a = mouse

        elif self.flag_B:

            self.point_b = mouse

        elif self.flag_C:

            try:
                self.input = int(inputbox.ask(screen, 'Scale all to'))

                global scale
                scale = self.input/length
                self.flag_C = False

            except ValueError:
                print "Not a number"

        elif self.flag_D:

            try:

                self.input_D = int(inputbox.ask(screen, 'Scale this to'))

                self.point_b[0] = (self.point_b[0] - self.point_a[0] )* (self.input_D / dim) + self.point_a[0]
                self.point_b[1] = (self.point_b[1] - self.point_a[1] )* (self.input_D / dim) + self.point_a[1]

                self.flag_D = False

            except ValueError:

                print "Not a number"

        elif self.flag_E:

            try:

                self.input_E = int(inputbox.ask(screen, 'Scale this to'))

                self.point_a[0] = (self.point_a[0] - self.point_b[0] )* (self.input_E / dim) + self.point_b[0]
                self.point_a[1] = (self.point_a[1] - self.point_b[1] )* (self.input_E / dim) + self.point_b[1]

                self.flag_E = False

            except ValueError:

                print "Not a number"


# ======================================================================================================================
#  The ModeSelect Class accepts input from the user


class ModeSelect:
    def __init__(self):

        self.mode = "None"

    def user_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # check if close button has been pressed

                pygame.quit()  # quits pygame
                quit()  # quits

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_b:

                    self.mode = "Beams"

                elif event.key == pygame.K_d:

                    self.mode = "Dimension"

                elif event.key == pygame.K_s:

                    self.mode = "Supports"

                elif event.key == pygame.K_f:

                    self.mode = "Forces"

# ======================================================================================================================
# The Beams class contains the parameters for beams


class Beams(Lines):
    def __init__(self, point_a, point_b, color):
        Lines.__init__(self, point_a, point_b, color)

# ======================================================================================================================
# The Forces class contains the parameters for a force vector


class Forces(Lines):
    def __init__(self, point_a, point_b, color):
        Lines.__init__(self, point_a, point_b, color)

# ======================================================================================================================
# The ReactiveForces class contains the parameters for the reaction forces on a beam.


class ReactiveForces(Lines):
    def __init__(self, point_a, point_b, color):
        Lines.__init__(self, point_a, point_b, color)

# ======================================================================================================================
# The Physics class calculates the reaction forces


# class Physics:
    # def __init__(self):

# ======================================================================================================================
if __name__ == '__main__':
    try:
        display = Screen()

        ui = ModeSelect()

        draw = Drawings()

        while True:

            ui.user_input()

            display.pane(ui.mode)

            draw.permanent_draw(display.screen, display.font)

            if ui.mode == "Beams":

                draw.temporary_draw(display.screen, display.font, ui.mode)

            elif ui.mode == "Forces":

                draw.temporary_draw(display.screen, display.font, ui.mode)

            elif ui.mode == "Dimension":

                draw.rescale(display.screen, ui.mode)

            pygame.display.update()

    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()

# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================

'''
class Main:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.screen.fill(white)
        pygame.display.set_caption("Draw Lines and Shit")

        self.myfont = pygame.font.SysFont("arial", 15)

        self.P1 = [0, 0]  # Place to store starting point of a line

        self.P2 = [0, 0]  # Place to store ending point of a line

        self.flag = False

    def main_thread(self):

        while True:
             
            self.screen.fill(white)

            self.user_input()

            self.draw()

            pygame.display.update()
    
            pygame.event.clear()

    def user_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # check if close button has been pressed
                pygame.quit()  # quits pygame
                quit()  # quits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print "Beams"
                    self.beam_thread()
                elif event.key == pygame.K_d:
                    print "Dimensions"
                    self.dimension()
                elif event.key == pygame.K_s:
                    print "Supports"
                    self.support(self.screen)
                elif event.key == pygame.K_f:
                    print "Forces"
                    self.forces_thread()

    def draw(self):

        for k in lines:
            k.draw(self.screen)

        for k in forces:
            k.draw(self.screen)

        for i in fixed_supports:
            i.draw_support(self.screen)

        for i in pinned_supports:
            i.draw_support(self.screen)

        for i in roller_supports:
            i.draw_support(self.screen)

    def beam_thread(self):

            while True:

                self.screen.fill(white)

                self.user_input()

                if (pygame.mouse.get_pressed()[0]) and (self.flag == False):
                    self.P1[:] = pygame.mouse.get_pos()
                    self.flag = True
                elif (pygame.mouse.get_pressed()[0]) and (self.flag == True):
                    self.P2[:] = pygame.mouse.get_pos()
                    if -10 < (self.P2[0] - self.P1[0]) < 10:
                        self.P2[0] = self.P1[0]
                    if -10 < (self.P2[1] - self.P1[1]) < 10:
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
                    if -10 < (self.P2[0] - self.P1[0]) < 10 :
                        self.P2[0] = self.P1[0]
                    if -10 < (self.P2[1] - self.P1[1]) < 10 :
                        self.P2[1] = self.P1[1]

                    lines.append(Lines(self.P1[:], self.P2[:], black))

                    self.flag = False

                self.draw()

                pygame.display.update()
    
                pygame.event.clear()

    def forces_thread(self):

        while True:

            self.screen.fill(white)

            self.user_input()

            self.draw()

            for k in lines:

                k.physics(self.screen)

            pygame.display.update()

            pygame.event.clear()

    def support(self, screen):

        display = screen

        support_type = "none"

        z = 0
        
        while supportRun:

            display.fill(white)

            x,y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # check if close button has been pressed
                    pygame.quit()  # quits pygame
                    quit()  # quits
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        print "Beams"
                        self.beam_thread()
                    elif event.key == pygame.K_d:
                        print "Dimensions"
                        self.dimension()

                    elif event.key == pygame.K_f:
                        print "Forces"
                        self.forces_thread()

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

            self.draw()

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

        while True:

            global scale

            self.screen.fill(white)

            self.user_input()

            self.draw()

            for k in lines:
                k.rescale(self.screen)

            for k in forces:
                k.rescale(self.screen)

            pygame.display.update()
    
            pygame.event.clear()


class Lines:

    def __init__(self, p1, p2, color):

        self.p1 = p1
        self.p2 = p2

        self.P1 = [0, 0]  # Place to store starting point of a line

        self.P2 = [0, 0]  # Place to store ending point of a line

        self.color = color
        self.myfont = pygame.font.SysFont("arial", 15)

        self.flag = False

        self.flag_A = False
        self.flag_B = False
        self.flag_C = False

        self.flag_D = False
        self.flag_E = False

        self.input = 0

    def draw(self, screen):

        self.length = np.linalg.norm(np.array(self.p1) - np.array(self.p2))

        self.dim = scale*self.length

        pygame.draw.line(screen, self.color, self.p1,  self.p2, 3)
        pygame.draw.circle(screen, self.color, [int(self.p1[0]), int(self.p1[1])], 5, 5)
        pygame.draw.circle(screen, self.color, [int(self.p2[0]), int(self.p2[1])], 5, 5)

        final_length = self.myfont.render(str("%.1f" % self.dim), 1, black)

        screen.blit(final_length, self.p1)

    def physics(self, screen):

        mouse = pygame.mouse.get_pos()

        dist_A = np.linalg.norm(mouse - np.array(self.p1))

        dist_B = np.linalg.norm(mouse - np.array(self.p2))

        if (pygame.mouse.get_pressed()[0]) and (not self.flag) and (round(dist_A + dist_B) == round(self.length)):

            self.P1[:] = pygame.mouse.get_pos()
            self.flag = True

        elif (pygame.mouse.get_pressed()[0]) and (self.flag == True):

            self.P2[:] = pygame.mouse.get_pos()

            if -10 < (self.P2[0] - self.P1[0]) < 10:
                self.P2[0] = self.P1[0]

            if -10 < (self.P2[1] - self.P1[1]) < 10:
                self.P2[1] = self.P1[1]

            pygame.draw.line(screen, blue, self.P1[:], self.P2[:], 3)
            pygame.draw.circle(screen, blue, [int(self.P1[0]), int(self.P1[1])], 5, 5)
            pygame.draw.circle(screen, blue, [int(self.P2[0]), int(self.P2[1])], 5, 5)
            length = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))
            dim = scale_forces * length
            temp_length = self.myfont.render(str("%.1f" % dim), 1, red)

            screen.blit(temp_length, self.P1[:])

        elif (pygame.mouse.get_pressed()[0] == False) and (self.flag == True):

            self.P2[:] = pygame.mouse.get_pos()

            if -10 < (self.P2[0] - self.P1[0]) < 10:
                self.P2[0] = self.P1[0]

            if -10 < (self.P2[1] - self.P1[1]) < 10:
                self.P2[1] = self.P1[1]

            forces.append(Forces(self.P1[:], self.P2[:], blue))

            self.flag = False

        #toque = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:])) *

        #self.length
        lever_arm = np.linalg.norm

    def rescale(self, screen):

        mouse = pygame.mouse.get_pos()

        dist_A = np.linalg.norm(mouse - np.array(self.p1))

        dist_B = np.linalg.norm(mouse - np.array(self.p2))

        if (round(dist_A + dist_B) == round(self.length)) or ((dist_A < 6) or (dist_B < 6)):

            pygame.draw.line(screen, red, self.p1, self.p2, 3)
            pygame.draw.circle(screen, red, [int(self.p1[0]), int(self.p1[1])], 5, 5)
            pygame.draw.circle(screen, red, [int(self.p2[0]), int(self.p2[1])], 5, 5)

            if (dist_A < 6) and (pygame.mouse.get_pressed()[0]):

                self.flag_A = True

            elif (dist_B < 6) and (pygame.mouse.get_pressed()[0]):

                self.flag_B = True

            elif (round(dist_A + dist_B) == round(self.length)) and (pygame.mouse.get_pressed()[0]):

                self.flag_C = True

            elif (dist_A < 6) and (pygame.mouse.get_pressed()[2]):

                self.flag_D = True

            elif (dist_B < 6) and (pygame.mouse.get_pressed()[2]):

                self.flag_E = True

            elif (pygame.mouse.get_pressed()[0]) == False:

                self.flag_A = False
                self.flag_B = False

        if self.flag_A:

            self.p1 = mouse

        elif self.flag_B:

            self.p2 = mouse

        elif self.flag_C:

            try:
                self.input = int(inputbox.ask(screen, 'Scale all to'))

                global scale
                scale = self.input/self.length
                self.flag_C = False

            except ValueError:
                print "Not a number"

        elif self.flag_D:

            try:

                self.input_D = int(inputbox.ask(screen, 'Scale this to'))

                self.p2[0] = (self.p2[0] - self.p1[0] )* (self.input_D / self.dim) + self.p1[0]
                self.p2[1] = (self.p2[1] - self.p1[1] )* (self.input_D / self.dim) + self.p1[1]

                self.flag_D = False

            except ValueError:

                print "Not a number"

        elif self.flag_E:

            try:

                self.input_E = int(inputbox.ask(screen, 'Scale this to'))

                self.p1[0] = (self.p1[0] - self.p2[0] )* (self.input_E / self.dim) + self.p2[0]
                self.p1[1] = (self.p1[1] - self.p2[1] )* (self.input_E / self.dim) + self.p2[1]

                self.flag_E = False

            except ValueError:

                print "Not a number"

class Support:

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
                                ((self.x, self.y), (self.x-15, self.y+20),
                                (self.x+15, self.y+20)))

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


class Forces:

    p1 = 0
    p2 = 0
    color = [0, 0, 0]

    def __init__(self, p1, p2, color):

        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.myfont = pygame.font.SysFont("arial", 15)

        self.flag_A = False
        self.flag_B = False
        self.flag_C = False

        self.flag_D = False
        self.flag_E = False

        self.input = 0

    def draw(self, screen):

        self.length = np.linalg.norm(np.array(self.p1) - np.array(self.p2))

        self.dim = scale_forces*self.length

        pygame.draw.line(screen, self.color, self.p1,  self.p2, 3)
        pygame.draw.circle(screen, self.color, [int(self.p1[0]), int(self.p1[1])], 5, 5)
        pygame.draw.circle(screen, self.color, [int(self.p2[0]), int(self.p2[1])], 5, 5)

        final_length = self.myfont.render(str("%.1f" % self.dim), 1, black)

        screen.blit(final_length, self.p1)

    def physics(self, screen):

        print "Physics!!!"

    def rescale(self, screen):

        mouse = pygame.mouse.get_pos()

        dist_A = np.linalg.norm(mouse - np.array(self.p1))

        dist_B = np.linalg.norm(mouse - np.array(self.p2))

        if (round(dist_A + dist_B) == round(self.length)) or ((dist_A < 6) or (dist_B < 6)):

            pygame.draw.line(screen, blue, self.p1, self.p2, 3)
            pygame.draw.circle(screen, blue, [int(self.p1[0]), int(self.p1[1])], 5, 5)
            pygame.draw.circle(screen, blue, [int(self.p2[0]), int(self.p2[1])], 5, 5)

            if (dist_A < 6) and (pygame.mouse.get_pressed()[0]):

                self.flag_A = True

            elif (dist_B < 6) and (pygame.mouse.get_pressed()[0]):

                self.flag_B = True

            elif (round(dist_A + dist_B) == round(self.length)) and (pygame.mouse.get_pressed()[0]):

                self.flag_C = True


            elif (dist_A < 6) and (pygame.mouse.get_pressed()[2]):

                self.flag_D = True

            elif (dist_B < 6) and (pygame.mouse.get_pressed()[2]):

                self.flag_E = True

            elif (pygame.mouse.get_pressed()[0]) == False:

                self.flag_A = False
                self.flag_B = False

        if self.flag_A:

            self.p1 = mouse

        elif self.flag_B:

            self.p2 = mouse

        elif self.flag_C:

            try:
                self.input = int(inputbox.ask(screen, 'Scale all to'))

                global scale_forces
                scale_forces = self.input/self.length
                self.flag_C = False

            except ValueError:
                print "Not a number"

        elif self.flag_D:

            try:

                self.input_D = int(inputbox.ask(screen, 'Scale this to'))

                self.p2[0] = (self.p2[0] - self.p1[0] )* (self.input_D / self.dim) + self.p1[0]
                self.p2[1] = (self.p2[1] - self.p1[1] )* (self.input_D / self.dim) + self.p1[1]

                self.flag_D = False

            except ValueError:

                print "Not a number"

        elif self.flag_E:

            try:

                self.input_E = int(inputbox.ask(screen, 'Scale this to'))

                self.p1[0] = (self.p1[0] - self.p2[0] )* (self.input_E / self.dim) + self.p2[0]
                self.p1[1] = (self.p1[1] - self.p2[1] )* (self.input_E / self.dim) + self.p2[1]

                self.flag_E = False

            except ValueError:

                print "Not a number"


if __name__ == '__main__':
    
    try:

        while True:
            sim = Main()
            sim.main_thread()
        
    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()'''