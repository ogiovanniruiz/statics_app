import pygame

import numpy as np

import math

import inputbox

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]
ORANGE = (255, 102, 0)

scale = 1

# ======================================================================================================================
# The Lines Class contains parameters for general lines


class Lines:

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

    def rescale(self, screen):

        mouse = pygame.mouse.get_pos()

        dist_a = np.linalg.norm(mouse - np.array(self.point_a))

        dist_b = np.linalg.norm(mouse - np.array(self.point_b))

        length = np.linalg.norm(np.array(self.point_a) - np.array(self.point_b))

        global scale

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

            elif not pygame.mouse.get_pressed()[0]:

                self.flag_A = False
                self.flag_B = False

        if self.flag_A:

            self.point_a[:] = mouse

            if -10 < (self.point_a[0] - self.point_b[0]) < 10:

                self.point_a[0] = self.point_b[0]

            if -10 < (self.point_a[1] - self.point_b[1]) < 10:

                self.point_a[1] = self.point_b[1]

        elif self.flag_B:

            self.point_b[:] = mouse

            if -10 < (self.point_b[0] - self.point_a[0]) < 10:

                self.point_b[0] = self.point_a[0]

            if -10 < (self.point_b[1] - self.point_a[1]) < 10:

                self.point_b[1] = self.point_a[1]

        elif self.flag_C:

            try:
                self.input = int(inputbox.ask(screen, 'Scale all to'))

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
# The Beams class contains the parameters for beams


class Beams(Lines):
    def __init__(self, point_a, point_b, color):
        Lines.__init__(self, point_a, point_b, color)

        self.over_beam = False

    def beam_check(self):

        mouse = pygame.mouse.get_pos()

        dist_a = np.linalg.norm(mouse - np.array(self.point_a))

        dist_b = np.linalg.norm(mouse - np.array(self.point_b))

        length = np.linalg.norm(np.array(self.point_a) - np.array(self.point_b))

        if round(dist_a + dist_b) == round(length):

            self.over_beam = True

        else:

            self.over_beam = False

# ======================================================================================================================
# The Forces class contains the parameters for a force vector


class Forces(Lines):
    def __init__(self, point_a, point_b, color):
        Lines.__init__(self, point_a, point_b, color)

    def draw_triangles(self, screen):

        theta = math.atan2((self.point_a[1] - self.point_b[1]), (self.point_a[0] - self.point_b[0]))

        p2x = int(self.point_a[0] - 50 * math.cos(theta + 0.2))
        p2y = int(self.point_a[1] - 50 * math.sin(theta + 0.2))
        p3x = int(self.point_a[0] - 50 * math.cos(theta - 0.2))
        p3y = int(self.point_a[1] - 50 * math.sin(theta - 0.2))

        pygame.draw.polygon(screen, blue, (self.point_a, (p2x, p2y), (p3x, p3y)))

# ======================================================================================================================
# The ReactiveForces class contains the parameters for the reaction forces on a beam.


class ReactiveForces(Lines):
    def __init__(self, point_a, point_b, color):
        Lines.__init__(self, point_a, point_b, color)

    #def draw_reaction_forces(self):