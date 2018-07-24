import pygame

SCREENSIZE = [800, 800]  # Size of our output display

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]
ORANGE = (255, 102, 0)

mode_pos = [100, 100]

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