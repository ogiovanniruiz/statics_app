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

    def permanent_draw(self, screen, font, mode):

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
