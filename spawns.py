import vars as v

from pygame.math import Vector2

lane_spacing = 0.835

lane_c = Vector2(v.DISPLAY_SIZE[0] / 2, 400)
lane_l = Vector2(lane_c.x - (lane_c.x / 2) * lane_spacing, lane_c.y)
lane_r = Vector2(lane_c.x + (lane_c.x / 2) * lane_spacing, lane_c.y)

lanes = (lane_l, lane_c, lane_r)