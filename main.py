import pygame
import sys
import os

from enum import Enum
from typing import Dict
from pygame import Surface, Rect
from pygame.math import Vector2

pygame.init()

DISPLAY_SIZE = (400, 500)
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
CLOCK = pygame.time.Clock()

def print_warning(n = "?"):
    """
    shorthand for printing out a warning message.
    """

    print("{S} {N}".format(S = "[!]", N = n))

def import_image(filepath: str, scale = 1) -> Surface:
    """
    imports an image as surface and applies a scale to it if specified.
    """
    
    if not os.path.exists(filepath):
        print_warning("image {F} not found!".format(F = filepath))
        return None

    img = pygame.image.load(filepath).convert_alpha()

    return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

def lerp(a = 0, b = 0, t = 0.125):
    """
    lerps without the need to use a vector2
    """

    return a + (t - 0) * (b - a) / (1 - 0)

#region assets
car = import_image('player.png', 3)
#endregion

#region lanes & vehicle spawns
lane_spacing = 1

lane_c = Vector2(DISPLAY_SIZE[0] / 2, 400)
lane_l = Vector2(lane_c.x - (lane_c.x / 2) * lane_spacing, lane_c.y)
lane_r = Vector2(lane_c.x + (lane_c.x / 2) * lane_spacing, lane_c.y)

spawn_c = Vector2(lane_c.x, 0)
spawn_l = Vector2(lane_l.x, 0)
spawn_r = Vector2(lane_r.x, 0)

lanes = (lane_l, lane_c, lane_r)
current_lane = 1
#endregion

#region input
class Direction(Enum):
    LEFT = -1
    RIGHT = 1

get_l = False
get_r = False

can_press_l = False
can_press_r = False

l_pressed = False
r_pressed = False

last_direction: Direction = Direction.LEFT
#endregion

#region player
pos = Vector2(lane_c)
__pos = pos
rot = 0
__rot = rot
#endregion

while True:
    #pygame opening
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    DELTA_TIME = CLOCK.tick(60) / 1000
    DISPLAY.fill((0, 0, 0))

    #position & rotate player
    __rot = Vector2.magnitude(lanes[current_lane] - pos) * 0.75 * last_direction.value
    __pos = lanes[current_lane]
    
    pos = lerp(pos, __pos)
    rot = lerp(rot, __rot)
    
    #draw player --NOTE define vars globally for performance
    player = pygame.transform.rotate(car, rot)
    
    player_rect = player.get_rect()
    player_rect.center = pos
    
    DISPLAY.blit(player, player_rect)

    #draw lane positons --NOTE debug
    pygame.draw.circle(DISPLAY, (255, 255, 255), lane_c, 5)
    pygame.draw.circle(DISPLAY, (255, 255, 255), lane_l, 5)
    pygame.draw.circle(DISPLAY, (255, 255, 255), lane_r, 5)

    #draw vehicle spawns --NOTE debug
    pygame.draw.circle(DISPLAY, (255, 0, 0), spawn_c, 5)
    pygame.draw.circle(DISPLAY, (255, 0, 0), spawn_l, 5)
    pygame.draw.circle(DISPLAY, (255, 0, 0), spawn_r, 5)
    
    #input
    get_l = pygame.key.get_pressed()[pygame.K_a]
    get_r = pygame.key.get_pressed()[pygame.K_d]
    
    can_press_l = (current_lane > 0) and not l_pressed
    can_press_r = (current_lane < len(lanes) - 1) and not r_pressed

    if get_l and can_press_l: 
        current_lane -= 1
        last_direction = Direction.RIGHT
        
        l_pressed = True
    
    elif not get_l:
        l_pressed = False
    
    if get_r and can_press_r:
        current_lane += 1
        last_direction = Direction.LEFT
        
        r_pressed = True

    elif not get_r:
        r_pressed = False

    #pygame closing
    pygame.display.update()