import vars as v
import assets as a
import road as rd
import game_manager as gm

from random import randint
from pygame import Surface, Rect
from pygame.math import Vector2

obstacle_assets = [
    a.police,
    a.car_g,
    a.car_o,
    a.car_r,
    a.car_y
]

#NOTE we spawn at -50 so cars spawn offscreen
obstacle_spawns = [
    Vector2(rd.lane_l.x, -50), 
    Vector2(rd.lane_c.x, -50), 
    Vector2(rd.lane_r.x, -50)
]

obstacles = []
spawn_ticks = 1 #amt of ticks before a vehicle spawns
spawn_ticks_t = spawn_ticks #temp current spawntick goal for next vehicle to spawn
blocked_spawn = -1 #which lane is blocked from spawning enemies? should be a val between 0 and 3; anything else means no lanes are blocked

class Obstacle:
    texture: Surface = None
    hitbox: Rect = None
    
    pos: Vector2 = None
    speed = 300

    __drop_shadow_rect: Rect = None

    def __init__(self, texture: Surface, start_pos: Vector2) -> None:
        self.texture = texture.copy()
        self.hitbox = texture.get_rect()

        self.pos = Vector2(start_pos)

        self.__drop_shadow_rect = a.shadow.get_rect()

        #initialize rects --NOTE this prevents flickering when cars are instantiated!
        self.hitbox.center = self.pos
        self.__drop_shadow_rect.center = self.pos

    def update(self) -> None:
        #delete this obstacle if out of screen bounds (NOTE +100 is just for ensuring object doesn't die onscreen no matter the size)
        if self.pos.y >= v.DISPLAY_SIZE[1] + 100:
            global obstacles
            obstacles.remove(self)
            del self
            return
        
        #position (drop shadow)
        self.__drop_shadow_rect.center = self.pos
        
        #position (texture)
        self.pos.y += (self.speed + (gm.speed - gm.base_speed)) * vars.DELTA_TIME #y pos vel increment is obstacle base speed (300) + the difference between current game speed and base game speed
        self.hitbox.center = self.pos

    def draw(self) -> None:        
        # #draw hitbox --NOTE for debugging
        # pygame.draw.rect(DISPLAY, (0, 0, 255), self.rect)
        
        #drawing (drop shadow)
        v.DISPLAY.blit(a.shadow, self.__drop_shadow_rect)

        #drawing (texture)
        v.DISPLAY.blit(self.texture, self.hitbox)

def RandomExclude(a, b, e) -> int:
    """
    Generates a random number between a, b inclusively excluding e.
    """
    
    r = randint(a, b)
    if r != e:
        return r
    return RandomExclude(a, b, e)

def SpawnObstacle() -> None:
    """
    Spawns an obstacle.
    """

    obstacles.append(
        Obstacle(
            obstacle_assets[randint(0, len(obstacle_assets) - 1)],
            obstacle_spawns[RandomExclude(0, len(obstacle_spawns) - 1, blocked_spawn)]
        )
    )