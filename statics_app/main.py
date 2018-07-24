from screen import Screen

from draw_lines import *

from lines import *

from mode_select import *

# ======================================================================================================================
if __name__ == '__main__':
    try:
        display = Screen()

        ui = ModeSelect()

        draw_lines = DrawLines()

        while True:

            ui.user_input()

            display.pane(ui.mode)

            draw_lines.permanent_draw_all(display.screen, display.font)

            if ui.mode == "Beams" or ui.mode == "Forces":

                draw_lines.temporary_draw(display.screen, display.font, ui.mode)

            elif ui.mode == "Dimension":

                draw_lines.rescale_all(display.screen)

            for k in beams:
                k.beam_check()

            pygame.display.update()

    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()
