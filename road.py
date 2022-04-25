import vars as v
import assets as a
import game_manager as gm

from pygame.math import Vector2

road_rect_a = a.road.get_rect()
road_rect_b = a.road.get_rect()

road_pos_a = Vector2(v.DISPLAY_SIZE[0] / 2, v.DISPLAY_SIZE[1] / 2)
road_pos_b = road_pos_a - Vector2(0, a.road.get_height())

road_vel = gm.speed #current road vel
road_dsp = a.road.get_height() * 2