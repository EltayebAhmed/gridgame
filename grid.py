try:
    import pygame
except ImportError:
    print("Pygame is not installed, attempting to install pygame, this will fail if you do not have an active internet "+
          "connection")
    import sys, subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pygame"])
    print("Pygame Installed successfully. Python will now shut down. Next time you import the script it should run "
          "successfully")
    print("Quiting ...........")
    quit()


class GridGui:
    """A Simple Interface for creating games that use 2d square grid user interfaces. This class provides support for
    interacting with the screen as a 2D grid of cells, as well as capturing mouse clicks and keyboard events. Recognized
    color strings are: 'white', 'black', 'red', 'green', 'blue', 'yellow', 'pink', 'purple'"""
    def __init__(self, dimensions, cell_size, origin="bottom_left"):
        """
        Parameters

        -----------

        `dimensions` : tuple of two integers
                        The first component is the width of screen and the second component is the height of the screen.
                        Both height and width are specified in the number of cells. Both must be positive integers

        `cell_size` : tuple of two integers
                        The first component is the width of each individual cell in pixels. The second component is the
                        height of each cell in pixels. Both width and height must be positive non zero integers

        `origin` : string
                    Currently has no effect. Will be documented after the feature is finished

        """
        self._origin = origin
        self._dim = dimensions
        self._cell_size = cell_size
        self._width = cell_size[0] * dimensions[0]
        self._height = cell_size[1] * dimensions[1]
        if dimensions[0] <= 0 or dimensions[1] <= 0:
            raise ValueError("Both dimensions must be positive")
        if cell_size[0] <= 0 or cell_size[1] <= 0:
            raise ValueError("Both dimensions of cell_size must be positive")
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._fps = 30
        self._colors_table = {"white": (255, 255, 255), "black": (0, 0, 0),
                              "red": (255, 0, 0), "green": (0, 255, 0),
                              "blue": (0, 0, 255), "yellow": (255, 255, 0),
                              "pink": (255, 20, 147), "purple": (128, 0, 128)}
        self._screen.fill(self._colors_table["white"])
        self._clock = pygame.time.Clock()
        self._key_presses = []
        self._clicks = []
        self._mouse_motion = []
        self._key_map = {768: 'ALT', 8192: 'CAPS', 192: 'CTRL', 256: 'KP0', 64: 'AT', 1024: 'LMETA', 1: 'LSHIFT',
                         3072: 'META', 16384: 'MODE', 0: 'UNKNOWN', 4096: 'NUM', 512: 'RALT', 128: 'RCTRL',
                         2048: 'RMETA', 2: 'RSHIFT', 3: 'SHIFT', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5',
                         54: '6', 55: '7', 56: '8', 57: '9', 97: 'A', 38: 'AMPERSAND', 42: 'ASTERISK', 98: 'B',
                         96: 'BACKQUOTE', 92: 'BACKSLASH', 8: 'BACKSPACE', 318: 'BREAK', 99: 'C', 301: 'CAPSLOCK',
                         94: 'CARET', 12: 'CLEAR', 58: 'COLON', 44: 'COMMA', 100: 'D', 127: 'DELETE', 36: 'DOLLAR',
                         274: 'DOWN', 101: 'E', 279: 'END', 61: 'EQUALS', 27: 'ESCAPE', 321: 'EURO', 33: 'EXCLAIM',
                         102: 'F', 282: 'F1', 291: 'F10', 292: 'F11', 293: 'F12', 294: 'F13', 295: 'F14', 296: 'F15',
                         283: 'F2', 284: 'F3', 285: 'F4', 286: 'F5', 287: 'F6', 288: 'F7', 289: 'F8', 290: 'F9',
                         103: 'G', 62: 'GREATER', 104: 'H', 35: 'HASH', 315: 'HELP', 278: 'HOME', 105: 'I',
                         277: 'INSERT', 106: 'J', 107: 'K', 257: 'KP1', 258: 'KP2', 259: 'KP3', 260: 'KP4', 261: 'KP5',
                         262: 'KP6', 263: 'KP7', 264: 'KP8', 265: 'KP9', 267: 'KP', 271: 'KP', 272: 'KP', 269: 'KP',
                         268: 'KP', 266: 'KP', 270: 'KP', 108: 'L', 308: 'LALT', 323: 'LAST', 306: 'LCTRL', 276: 'LEFT',
                         91: 'LEFTBRACKET', 40: 'LEFTPAREN', 60: 'LESS', 310: 'LMETA', 304: 'LSHIFT', 311: 'LSUPER',
                         109: 'M', 319: 'MENU', 45: 'MINUS', 313: 'MODE', 110: 'N', 300: 'NUMLOCK', 111: 'O', 112: 'P',
                         281: 'PAGEDOWN', 280: 'PAGEUP', 19: 'PAUSE', 46: 'PERIOD', 43: 'PLUS', 320: 'POWER',
                         316: 'PRINT', 113: 'Q', 63: 'QUESTION', 39: 'QUOTE', 34: 'QUOTEDBL', 114: 'R', 307: 'RALT',
                         305: 'RCTRL', 13: 'RETURN', 275: 'RIGHT', 93: 'RIGHTBRACKET', 41: 'RIGHTPAREN', 309: 'RMETA',
                         303: 'RSHIFT', 312: 'RSUPER', 115: 'S', 302: 'SCROLLOCK', 59: 'SEMICOLON', 47: 'SLASH',
                         32: 'SPACE', 317: 'SYSREQ', 116: 'T', 9: 'TAB', 117: 'U', 95: 'UNDERSCORE', 273: 'UP',
                         118: 'V', 119: 'W', 120: 'X', 121: 'Y', 122: 'Z'}

    def _update_state(self):
        self._enque_events()
        pygame.display.flip()

    def tick(self):
        """This function waits for time approximately equal to 1/fps. This function must be called every time after a
        full screen update has been completed"""
        self._update_state()
        self._clock.tick(self._fps)

    def set_fps(self, fps):
        """
        Sets the frame rate of the game. For game to refresh at correct rate the `tick` method must be invoked after
        every time a screen update is completed

        ------------

        Parameters

        `fps` : float or integer
                Number of frames to display per second, valid values are 0 < `fps` <= 60"""
        if not (isinstance(fps, float) or isinstance(fps, int)):
            raise ValueError("fps must be a number")
        if not fps > 0 and fps < 60:
            raise ValueError("fps must be strictly greater than 0 and less than 60")
        self._fps = fps

    def fill(self, color):
        """Fill the entire screen with `color`

        ----------

        Parameters
        `color` : Known color string or RGB tuple of ints
                  known colors strings can be found at the beginning of the documentation of this class
                  RGB tuples are tuples that contain 3 integers. 0 <= each integer <= 255"""
        if isinstance(color, str):
            try:
                color = self._colors_table[color]
            except KeyError:
                raise ValueError(("Unrecognize color \"%s\" " % color) + \
                                 "\n Known colors are RGB tuples or :" + \
                                 ",".join(self._colors_table.keys()))
        # TODO validate RGB color
        self._screen.fill(color)
        self._update_state()

    def color_square(self, position, color):
        """Color the square `position` with color


        ----------

        Parameters
        `position` : Tuple pf two integers
        represent the x and y coordinated of the square to be colored. Coordinated represent a single block in the
        screen grid

        `color` : Known color string or RGB tuple of ints
          known colors strings can be found at the beginning of the documentation of this class
          RGB tuples are tuples that contain 3 integers. 0 <= each integer <= 255"""

        if not isinstance(position, tuple):
            raise ValueError("Position must be of type tuple and not %s " % str(type(position)))
        if not len(position) == 2:
            raise ValueError("Position must be a tuple of two components, not %i"  % len(position))
        if position[0] < 0 or position[1] < 0 or \
                position[0] >= self._dim[0] or position[1] >= self._dim[1]:
            raise ValueError("Invalid position %s, valid positions must fall inside grid with" % str(position) + \
                             " corners (0,0)inclusive and %s (not inclusive)" %  str(self._dim))

        position = self._to_pygame_coords(position)
        if not isinstance(color, (tuple, str)):
            raise ValueError("color must be a tuple of 3 integers or a known string")
        if isinstance(color, str):
            try:
                color = self._colors_table[color]
            except KeyError:
                raise ValueError((f"Unrecognize color \"{color}\" " ) + \
                                 "\n Known colors are RGB tuples or :" + \
                                 ",".join(self._colors_table.keys()))

        if not len(color) == 3 :
            raise ValueError("RGB color must be a tuple of length 3")
        if not all(map(lambda  x: isinstance(x, int), color)):
            raise ValueError("RGB color must be a tuple of integers")
        if not ((0 <= color[0] <= 255) and (0 <= color[0] <= 255) and (0 <= color[0] <= 255)):
            raise ValueError("RGB color tuple components must be >= 0 and <= 255")
        pygame.draw.rect(self._screen, color, pygame.Rect(position[0], position[1], *self._cell_size))

    def get_currently_pressed_keys(self):
        """Return a list of *currently* pressed keys

        ----------

        `returns` : a list of keys that are currently in the down position, example: ["K", "UP"].
         """
        self._update_state()
        keys = pygame.key.get_pressed()
        ret = [self._key_map[i] for i in range(len(keys)) if keys[i]]
        return ret

    def get_key_presses(self):
        """Returns a list of keys that have been pressed (transitioned from being up to being down) since the last time
        it was called

        ----------

        `returns` : a list of keys that have been pressed since it was last called, example: ["K", "UP"]
            """
        self._update_state()
        keys = self._key_presses[:]
        self._key_presses = []
        self._update_state()
        return keys

    def get_clicks(self):
        """Returns a list of _click events_ that happened since it was last called

       ----------

       `returns` : a list of click events that happened since it was last called. Each click event is a tuple with two
       components. The first component of each entry is a tuple of two ints, which returns contains the X and Y
       coordinates of the square that was clicked on. The second component is a string which tells which mouse button
       was used for the click. Possible values for the string are "LEFT", "RIGHT", "MIDDLE". An example return for this
       function is [((20, 35), "LEFT"), (12, "RIGHT")]
        """
        self._update_state()
        clicks = self._clicks[:]
        self._clicks = []
        self._update_state()
        return clicks

    def _to_pygame_coords(self, pos):
        return pos[0] * self._cell_size[0], pos[1] * self._cell_size[1]

    def _enque_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                self._key_presses.append(self._key_map[event.key])
            elif event.type == pygame.MOUSEBUTTONUP:
                key = {1: "LEFT", 3: "RIGHT", 2: "MIDDLE"}[event.button]
                pos = self._to_block_coords(event.pos)
                self._clicks.append((pos, key))

    def _to_block_coords(self, pos):
        return pos[0] // self._cell_size[0], pos[1] // self._cell_size[1]

