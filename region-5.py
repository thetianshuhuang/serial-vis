# example program using serial-vis.

import serial_vis
import pygame


# user vector graphics
# user commands go here
class user_vector_graphics(serial_vis.default_vector_graphics):

    coordinates = {
        "Red 1": (-4, 4),
        "Red 2": (-3, 3),
        "Red 3": (-2, 2),
        "Red 4": (-1, 1),
        "Green 1": (-4, 0),
        "Green 2": (-3, 0),
        "Green 3": (-2, 0),
        "Green 4": (-1, 0),
        "Blue 1": (-4, -4),
        "Blue 2": (-3, -3),
        "Blue 3": (-2, -2),
        "Blue 4": (-1, -1),
        "Cyan 1": (4, 4),
        "Cyan 2": (3, 3),
        "Cyan 3": (2, 2),
        "Cyan 4": (1, 1),
        "Magenta 1": (4, 0),
        "Magenta 2": (3, 0),
        "Magenta 3": (2, 0),
        "Magenta 4": (1, 0),
        "Yellow 1": (4, -4),
        "Yellow 2": (3, -3),
        "Yellow 3": (2, -2),
        "Yellow 4": (1, -1),
        "Red Box": (-5, 5),
        "Green Box": (-5, 0),
        "Blue Box": (-5, -5),
        "Cyan Box": (5, 5),
        "Magenta Box": (5, 0),
        "Yellow Box": (5, -5),
        "Grey Box": (0, 0)
    }

    def show_underlay(self):
        img = pygame.image.load("r5-field.png")
        self.screen.blit(img, (0, 0))

    def updatenode(self, instruction):

        pygame.draw.circle(
            self.screen,
            self.settings.colors[instruction[3]],
            self.coordinates[instruction[1]],
            10, 0)

        if(instruction[2] == "T"):
            pygame.draw.circle(
                self.screen,
                self.settings.colors[instruction[3]],
                self.coordinates[instruction[1]],
                12, 1)


# extend the serial_device class to add user definitions.
class r5_serial_vis(serial_vis.serial_vis):

    # graphics command registration
    user_commands = {"updatenode": ["s", "s", "s"]}
    graphics_class = user_vector_graphics

    # settings
    user_settings = {
        "scale": 10,
        "offset": (400, 400),
        "window_size": (800, 800),
        "colors": {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "magenta": (255, 0, 255),
            "grey": (128, 128, 128),
            "cyan": (0, 255, 255),
            "unknown": (128, 128, 128)
        }
    }


my_serial_device = r5_serial_vis(path="/dev/ttyACM0", baudrate=115200)

while(1):
    my_serial_device.update()
