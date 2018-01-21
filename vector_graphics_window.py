# vector_graphics_window.py
# create vector graphics rendering window

import pygame


# pygame window class

# methods:
# __init__              - takes **kwargs containing window settings
# update_screen         - updates the screen with the input frame_buffer object
# close_window          - cleanly close pygame
# instruction_error     - display error function
class vector_graphics_window:

    settings = {
        "window_size": (800, 600),
        "scale": 1.000,
        "offset": (0, 0),
        "store_frames": 100,
        "frame_limit": 60,
        "line_width": 2,
        "font": "arial",
        "events": {},
        "colors": {"black": (0, 0, 0),
                   "white": (255, 255, 255),
                   "background": (255, 255, 255)},
    }

    current_buffer_id = -1

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        # update settings
        self.settings.update(kwargs)

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.settings["window_size"])
        self.clock = pygame.time.Clock()

    #   --------------------------------
    #
    #   Update screen
    #
    #   --------------------------------
    def update_screen(self, frame_buffer):

        # return false if unsuccessful.
        if(frame_buffer.frame_id == self.current_buffer_id):
            return(False)

        # otherwise, draw the buffer
        else:
            self.current_buffer_id = frame_buffer.frame_id

            # clear pygame buffer
            self.screen.fill(self.colors["background"])

            for instruction in frame_buffer.instructions:

                # run through default draw functions
                try:
                    draw_function = getattr(self, instruction[0])
                    draw_function(instruction)
                # raise AttributeError
                # if the requested instruction doesn't exist.
                except AttributeError:
                    self.instruction_error(instruction)

        # display pygame buffer
        pygame.display.flip()

        # limit the fps
        self.clock.tick(self.frame_limit)

    #   --------------------------------
    #
    #   Close window
    #
    #   --------------------------------
    def close_window(self):

        pygame.display.quit()
        pygame.quit()

    #   --------------------------------
    #
    #   Display Error
    #
    #   --------------------------------
    def instruction_error(self, instruction):

        print("Unrecognized Opcode: " + instruction[0])
