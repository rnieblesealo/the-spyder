import pygame
import vars as v
import assets as a
import spawns as spa

from utils import Lerp
from random import randint
from pygame import Rect, Surface, PixelArray
from pygame.math import Vector2

spider_spawn_ticks = 25 #ticks it takes for spider to peek
spider_peek_ticks = 10 #ticks it takes for spider to go from peek -> attack
spider_attack_ticks = 1 #ticks spider takes attacking
spider_ticks_t = spider_spawn_ticks

class Spider:
    texture: Surface = None
    hitbox: Rect = None
    hitbox_fix = -20 #adjustment applied to rect w and h so its smaller/bigger

    state = 0 #0 for inactive, 1 for peeking, 2 for active
    current_lane = 1
    
    outline_color = (50, 50, 50)
    outline_width = 3 #keep below 5
    
    pos: Vector2 = None

    y_hidden = 0
    y_peeked = 0
    y_attack = 0

    __pos: Vector2 = None

    __outline: Surface = None

    def __init__(self, texture = a.spider, start_lane = 1) -> None:
        self.texture = texture.copy()
        self.hitbox = Rect(0, 0, self.texture.get_width() + self.hitbox_fix, self.texture.get_height() + self.hitbox_fix)
        
        #set vertical positions for different spider states
        self.y_hidden = DISPLAY_SIZE[1] + self.texture.get_height() / 2 + 10 #extra +10 is so spider outline isn't visible
        self.y_peeked = DISPLAY_SIZE[1]
        self.y_attack = spa.lanes[start_lane].y

        #reset current lane
        self.current_lane = start_lane
        
        #reset position
        self.pos = Vector2(spa.lanes[self.current_lane].x, self.y_hidden)
        self.__pos = self.pos.copy()

        #reset state
        self.state = 0

        #outline generation process
        
        #get binary bitmap surface of texture, convert it back to a surface 
        mask = pygame.mask.from_surface(self.texture)
        mask_surf = mask.to_surface() #--NOTE the result is a black & white surface where black represents transparent area and white represents filled area (of passed texture)
        
        #convert mask_surf into pixel data (numpy array) and replace white with desired color (this will be outline's color)
        mask_surf_pixels = PixelArray(mask_surf)
        mask_surf_pixels.replace((255, 255, 255), self.outline_color)
        
        self.__outline = mask_surf_pixels.make_surface()

    def reset(self) -> None:                        
        #reset state
        self.state = 0
        
        #reset position
        self.pos = Vector2(self.__pos.x, self.y_hidden)
        self.__pos = self.pos.copy()

        #set random new lane
        self.current_lane = randint(0, 2)

    #NOTE that drawing the outline is computationally expensive!
    def draw_outline(self, pos):
        #rotate outline surface
        c_outline = self.__outline.copy()
        
        #set outline colorkey (must do this every time we modify it)
        c_outline.set_colorkey((0, 0, 0))
                
        #draw outline (we shift it towards every direction to give outline effect)
        v.DISPLAY.blit(c_outline, (pos[0] - self.outline_width, pos[1]))
        v.DISPLAY.blit(c_outline, (pos[0] + self.outline_width, pos[1]))
        v.DISPLAY.blit(c_outline, (pos[0], pos[1] - self.outline_width))
        v.DISPLAY.blit(c_outline, (pos[0], pos[1] + self.outline_width))

    def update(self) -> None:       
        #position spider 
        global DISPLAY_SIZE
        match self.state:
            case 0:
                self.__pos.y = self.y_hidden
                pass
            case 1:
                self.__pos.y = self.y_peeked
                pass
            case 2:
                self.__pos.y = self.y_attack
                pass
            case _:
                self.__pos.y = self.y_hidden

        #use this for smooth x spider pos (looks ugly)
        #self.__pos.x = lanes[self.current_lane].x

        self.pos = Lerp(self.pos, self.__pos, 0.125 * v.DELTA_TIME * 60)
        
        #use this for instant x spider pos (looks nicer)
        self.pos.x = spa.lanes[self.current_lane].x

        #update rect (NOTE this isn't used for drawing, it's used for collision!)
        self.hitbox.center = self.pos
    
    def draw(self) -> None:
        #center texture around pos                
        texture_rect = self.texture.get_rect()
        texture_rect.center = self.pos
        
        #draw outline
        self.draw_outline(texture_rect.topleft)

        #draw texture
        v.DISPLAY.blit(self.texture, texture_rect)

spider = Spider()

def spider_time(spider = spider):
    global blocked_spawn
    
    if spider.state == 0:
        spider.state = 1
        spider.current_lane = randint(0, 2)
        if spider.current_lane == 1: #0 represents left, 1 center, 2 right
            blocked_spawn = 1 #block enemies from spawning at the center if spider goes here, this is more fair!
        a.s_peek.play()
        return spider_ticks_t + spider_peek_ticks
    elif spider.state == 1:
        spider.state = 2
        a.s_attack.play()
        return spider_ticks_t + spider_attack_ticks
    else:
        spider.state = 0
        blocked_spawn = -1 #reset blocked obstacle spawn to none
        a.s_hide.play()
        return spider_ticks_t + spider_spawn_ticks