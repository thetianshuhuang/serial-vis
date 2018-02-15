# keyboard_keybinds.py
# base class containing keybinds for basic typing

import pygame


class keyboard_keybinds:
    """
    Default keyboard keybinds for general typing

    Attributes
    ----------
    keymap
        Dictionary of pygame keys and their corresponding characters
    """

    keymap = {
        pygame.K_SPACE: [" ", " "],
        pygame.K_QUOTE: ["'", '"'],
        pygame.K_COMMA: [",", "<"],
        pygame.K_MINUS: ["-", "_"],
        pygame.K_PERIOD: [".", ">"],
        pygame.K_SLASH: ["/", "?"],
        pygame.K_0: ["0", ")"],
        pygame.K_1: ["1", "!"],
        pygame.K_2: ["2", "@"],
        pygame.K_3: ["3", "#"],
        pygame.K_4: ["4", "$"],
        pygame.K_5: ["5", "%"],
        pygame.K_6: ["6", "^"],
        pygame.K_7: ["7", "&"],
        pygame.K_8: ["8", "*"],
        pygame.K_9: ["9", "("],
        pygame.K_SEMICOLON: [";", ":"],
        pygame.K_EQUALS: ["=", "+"],
        pygame.K_LEFTBRACKET: ["[", "{"],
        pygame.K_BACKSLASH: ["\\", "|"],
        pygame.K_RIGHTBRACKET: ["]", "}"],
        pygame.K_a: ["a", "A"],
        pygame.K_b: ["b", "B"],
        pygame.K_c: ["c", "C"],
        pygame.K_d: ["d", "D"],
        pygame.K_e: ["e", "E"],
        pygame.K_f: ["f", "F"],
        pygame.K_g: ["g", "G"],
        pygame.K_h: ["h", "H"],
        pygame.K_i: ["i", "I"],
        pygame.K_j: ["j", "J"],
        pygame.K_k: ["k", "K"],
        pygame.K_l: ["l", "L"],
        pygame.K_m: ["m", "M"],
        pygame.K_n: ["n", "N"],
        pygame.K_o: ["o", "O"],
        pygame.K_p: ["p", "P"],
        pygame.K_q: ["q", "Q"],
        pygame.K_r: ["r", "R"],
        pygame.K_s: ["s", "S"],
        pygame.K_t: ["t", "T"],
        pygame.K_u: ["u", "U"],
        pygame.K_v: ["v", "V"],
        pygame.K_w: ["w", "W"],
        pygame.K_x: ["x", "X"],
        pygame.K_y: ["y", "Y"],
        pygame.K_z: ["z", "Z"]
    }
