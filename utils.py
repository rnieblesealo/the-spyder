import pygame
import os

from pygame import Surface

def PrintWarning(n = "None") -> None:
    """
    Prints out a warning message.
    """

    print("{S} {N}".format(S = "[!]", N = n))

def ImportImage(filepath: str, scale = 1) -> Surface:
    """
    Imports an image scaled by an integer factor.
    """
    
    if not os.path.exists(filepath):
        PrintWarning("image {F} not found!".format(F = filepath))
        return None

    img = pygame.image.load(filepath).convert_alpha()

    return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

def Lerp(a = 0, b = 0, t = 0.125) -> None:
    """
    Simple linear interpolation.
    """

    return a + t * (b - a)