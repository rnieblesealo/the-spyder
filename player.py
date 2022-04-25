import pygame
import vars as v
import assets as a
import spawns as spa
import spider as spi
import obstacles as o

from utils import PrintWarning, Lerp
from pygame import Surface, Rect, PixelArray
from game_manager import GameState
from pygame.math import Vector2
from enum import Enum

class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class Player:
    """
    player controller; only one per game instance!
    """

    texture: Surface = None
    hitbox: Rect = None
    hitbox_fix = -15 #adjustment applied to rect w and h so its smaller/bigger

    current_lane = 1
    last_direction: Direction = Direction.RIGHT
    
    pos: Vector2 = None
    rot = 0

    outline_color = (185, 185, 185)
    outline_width = 3 #keep below 5

    __pos: Vector2 = None
    __rot = 0

    __l_pressed = False
    __r_pressed = False

    __outline: Surface = None

    def __init__(self, texture = a.player, start_lane = 1) -> None:
        self.texture = texture.copy()
        self.hitbox = Rect(0, 0, self.texture.get_width() + self.hitbox_fix, self.texture.get_height() + self.hitbox_fix)

        self.current_lane = start_lane
        self.pos = Vector2(spa.lanes[self.current_lane])
        self.rot = 0

        #outline generation process
        
        #get binary bitmap surface of texture, convert it back to a surface 
        mask = pygame.mask.from_surface(self.texture)
        mask_surf = mask.to_surface() #--NOTE the result is a black & white surface where black represents transparent area and white represents filled area (of passed texture)
        
        #convert mask_surf into pixel data (numpy array) and replace white with desired color (this will be outline's color)
        mask_surf_pixels = PixelArray(mask_surf)
        mask_surf_pixels.replace((255, 255, 255), self.outline_color)
        
        self.__outline = mask_surf_pixels.make_surface()

    def reset_pos(self) -> None:
        """
        Resets the player's position and rotation to the central lane.
        """
        
        if self.current_lane == 1:
            return

        self.current_lane = 1
        
        self.pos = spa.lanes[1]
        self.rot = 0
        
        self.__pos = spa.lanes[1]
        self.__rot = 0

    def get_input(self) -> None:
        get_l = pygame.key.get_pressed()[pygame.K_a]
        get_r = pygame.key.get_pressed()[pygame.K_d]
        
        can_press_l = (self.current_lane > 0) and not self.__l_pressed
        can_press_r = (self.current_lane < len(spa.lanes) - 1) and not self.__r_pressed

        global state
        if state == GameState.IDLE:
            #reset position to center lane when game is idle
            self.reset_pos()

            #start game if input is received
            if get_l or get_r:
                PrintWarning("Starting Game!")
                state = GameState.GAME_ON

        #get left button input
        if get_l and can_press_l: 
            self.current_lane -= 1
            self.last_direction = Direction.RIGHT
            a.p_switch.play()
            
            self.__l_pressed = True
        
        elif not get_l:
            self.__l_pressed = False
        
        #get right button input
        if get_r and can_press_r:
            self.current_lane += 1
            self.last_direction = Direction.LEFT
            a.p_switch.play()
            
            self.__r_pressed = True

        elif not get_r:
            self.__r_pressed = False

    def update(self) -> None:       
        #position & rotate
        self.__rot = Vector2.magnitude(spa.lanes[self.current_lane] - self.pos) * 0.75 * self.last_direction.value
        self.__pos = spa.lanes[self.current_lane]
    
        self.rot = Lerp(self.rot, self.__rot, 0.125 * v.DELTA_TIME * 60)
        self.pos = Lerp(self.pos, self.__pos, 0.125 * v.DELTA_TIME * 60)

        #update rect (NOTE this isn't used for drawing, it's used for collision!)
        self.hitbox.center = self.pos

        #check for collision & gameover event handle
        global state
        if state == GameState.GAME_ON:
            for obstacle in o.obstacles:
                if self.hitbox.colliderect(obstacle.hitbox) or self.hitbox.colliderect(spi.spider.hitbox):                            
                    state = GameState.GAME_OVER
                    a.p_crash.play()

        #input
        self.get_input()
    
    #NOTE that drawing the outline is computationally expensive!
    def draw_outline(self, pos):
        #rotate outline surface
        r_outline = pygame.transform.rotate(self.__outline, self.rot)
        
        #set outline colorkey (must do this every time we modify it)
        r_outline.set_colorkey((0, 0, 0))
                
        #draw outline (we shift it towards every direction to give outline effect)
        v.DISPLAY.blit(r_outline, (pos[0] - self.outline_width, pos[1]))
        v.DISPLAY.blit(r_outline, (pos[0] + self.outline_width, pos[1]))
        v.DISPLAY.blit(r_outline, (pos[0], pos[1] - self.outline_width))
        v.DISPLAY.blit(r_outline, (pos[0], pos[1] + self.outline_width))

    def draw(self) -> None:
        # #draw hitbox --NOTE for debugging
        # pygame.draw.rect(DISPLAY, (0, 255, 0), self.rect)
        
        #rotate dropshadow
        r_shadow = pygame.transform.rotate(a.shadow, self.rot) #NOTE --move shadow_r to classvar?
        
        #center rotated dropshadow rect
        r_shadow_rect = r_shadow.get_rect()
        r_shadow_rect.center = self.pos
        
        #rotate texture
        r_texture = pygame.transform.rotate(self.texture, self.rot) #NOTE --move texture_r to classvar?
        
        #center rotated texture rect
        r_texture_rect = r_texture.get_rect()
        r_texture_rect.center = self.pos

        #draw dropshadow
        v.DISPLAY.blit(r_shadow, r_shadow_rect)
        
        #draw outline
        self.draw_outline(r_texture_rect.topleft)

        #draw texture
        v.DISPLAY.blit(r_texture, r_texture_rect)

player = Player()