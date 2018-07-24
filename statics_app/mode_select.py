import pygame

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
