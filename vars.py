from pygame import display, clock

DISPLAY_SIZE = (400, 500)
DISPLAY = None
CLOCK = None

def initialize():
    """
    Initialize display & clock. Call this after Pygame has been initialized!
    """
    
    global DISPLAY, CLOCK

    DISPLAY = display.set_mode(DISPLAY_SIZE)
    CLOCK = clock.Clock()