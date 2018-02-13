# command_line.py
# command line interface inside a pygame window

import pygame


#   --------------------------------
#
#   Command line
#
#   --------------------------------
class command_line:

    """
    Command line class
    """

    keymap = {
        pygame.K_SPACE: " ",
        pygame.K_EXCLAIM: "!",
        pygame.K_QUOTEDBL: '"',
        pygame.K_HASH: "#",
        pygame.K_DOLLAR: "$",
        pygame.K_AMPERSAND: "&",
        pygame.K_QUOTE: "'",
        pygame.K_LEFTPAREN: "(",
        pygame.K_RIGHTPAREN: ")",
        pygame.K_ASTERISK: "*",
        pygame.K_PLUS: "+",
        pygame.K_COMMA: ",",
        pygame.K_MINUS: "-",
        pygame.K_PERIOD: ".",
        pygame.K_SLASH: "/",
        pygame.K_0: "0",
        pygame.K_1: "1",
        pygame.K_2: "2",
        pygame.K_3: "3",
        pygame.K_4: "4",
        pygame.K_5: "5",
        pygame.K_6: "6",
        pygame.K_7: "7",
        pygame.K_8: "8",
        pygame.K_9: "9",
        pygame.K_COLON: ":",
        pygame.K_SEMICOLON: ";",
        pygame.K_LESS: "<",
        pygame.K_EQUALS: "=",
        pygame.K_GREATER: ">",
        pygame.K_QUESTION: "?",
        pygame.K_AT: "@",
        pygame.K_LEFTBRACKET: "[",
        pygame.K_BACKSLASH: "\\",
        pygame.K_RIGHTBRACKET: "]",
        pygame.K_CARET: "^",
        pygame.K_UNDERSCORE: "_",
        pygame.K_BACKQUOTE: "`",
        pygame.K_a: "a",
        pygame.K_b: "b",
        pygame.K_c: "c",
        pygame.K_d: "d",
        pygame.K_e: "e",
        pygame.K_f: "f",
        pygame.K_g: "g",
        pygame.K_h: "h",
        pygame.K_i: "i",
        pygame.K_j: "j",
        pygame.K_k: "k",
        pygame.K_l: "l",
        pygame.K_m: "m",
        pygame.K_n: "n",
        pygame.K_o: "o",
        pygame.K_p: "p",
        pygame.K_q: "q",
        pygame.K_r: "r",
        pygame.K_s: "s",
        pygame.K_t: "t",
        pygame.K_u: "u",
        pygame.K_v: "v",
        pygame.K_w: "w",
        pygame.K_x: "x",
        pygame.K_y: "y",
        pygame.K_z: "z",
    }

    # track capslock mode
    is_capslock = False

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings):

        """
        Create new command line instance.
        """

        self.settings = settings
        self.current_index = 0

        self.font = pygame.font.SysFont(
            self.settings.font, self.settings.font_size)
        self.line_contents = ""

    #   --------------------------------
    #
    #   Update
    #
    #   --------------------------------
    def update(self):

        """
        Update command line
        """

        str_to_add = ""
        caps = self.is_capslock

        for event in pygame.event.get():

            # check control keys
            if(event.type == pygame.KEYDOWN):

                # backspace
                if(event.type == pygame.K_BACKSPACE):
                    if(len(self.line_contents) > 0):
                        self.line_contents = self.line_contents[:-1]

                # escape
                if(event.type == pygame.K_ESCAPE):
                    pass
                    # exit command line mode

                # enter
                if(event.type == pygame.K_RETURN):
                    pass
                    # return the line and exit command line mode

                # left arrow
                if(event.type == pygame.K_LEFT):
                    if(self.current_index > 0):
                        self.current_index -= 1

                # right arrow
                if(event.type == pygame.K_RIGHT):
                    if(self.current_index < len(self.line_contents)):
                        self.current_index += 1

                # shift
                if(event.type == pygame.K_RSHIFT or
                   event.type == pygame.K_LSHIFT):
                    caps = not caps

                # capslock
                if(event.type == pygame.K_CAPSLOCK):
                    self.is_capslock = not self.is_capslock

            # append key to the string
            if event.type in self.keymap:
                str_to_add += self.keymap[event.type]
                self.current_index += 1

        # make caps if applicable
        if(caps):
            str_to_add.upper()

    #   --------------------------------
    #
    #   Get text object
    #
    #   --------------------------------
    def get_text_object(self):

        """
        Get text object corresponding to the current line
        """

        textframe = self.font.render(
            self.line_contents, False, self.settings.colors["black"])

        return(textframe)
