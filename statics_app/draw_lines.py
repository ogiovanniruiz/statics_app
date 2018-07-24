from main import *

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]
ORANGE = (255, 102, 0)

scale = 1

scale_forces = 1

beams = []  # A list containing lines

forces = []  # A List containing force vectors

# =======================================================================================================================
# The DrawLiens class draws force vectors and beam lines


class DrawLines:
    def __init__(self):

        self.color = [0, 0, 0]

        self.P1 = [0, 0]

        self.P2 = [0, 0]

        self.point_a = [0, 0]

        self.flag = False

    def temporary_draw(self, screen, font, mode):

        length = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))

        if (pygame.mouse.get_pressed()[0]) and (not self.flag):

            if all(k.over_beam == False for k in beams):

                flag = False

            else:
                
                flag = True

            print flag

            if mode == "Forces" and flag:

                self.P1[:] = pygame.mouse.get_pos()

                self.flag = True

            elif mode == "Beams":

                self.P1[:] = pygame.mouse.get_pos()

                self.flag = True

            else:

                self.flag = False

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

                theta = math.atan2((self.P1[1] - self.P2[1]), (self.P1[0] - self.P2[0]))

                p2x = int(self.P1[0] - 50*math.cos(theta + 0.2))
                p2y = int(self.P1[1] - 50*math.sin(theta + 0.2))
                p3x = int(self.P1[0] - 50*math.cos(theta - 0.2))
                p3y = int(self.P1[1] - 50*math.sin(theta - 0.2))

                pygame.draw.polygon(screen, green, (self.P1, (p2x, p2y), (p3x, p3y)))

            pygame.draw.line(screen, self.color, self.P1[:], self.P2[:], 3)

            pygame.draw.circle(screen, self.color, [int(self.P1[0]), int(self.P1[1])], 5, 5)

            pygame.draw.circle(screen, self.color, [int(self.P2[0]), int(self.P2[1])], 5, 5)

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

    def permanent_draw_all(self, screen, font):

        for k in beams:
            k.permanent_draw(screen, font)

        for k in forces:
            k.permanent_draw(screen, font)

        for k in forces:
            k.draw_triangles(screen)

    def rescale_all(self, screen):

        for k in beams:
            k.rescale(screen)

        for k in forces:
            k.rescale(screen)
