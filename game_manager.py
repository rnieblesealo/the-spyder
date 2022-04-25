import os

from enum import Enum

class GameState(Enum):
    IDLE = 0
    GAME_ON = 1
    GAME_OVER = 2

def get_highscore(in_int = False) -> int:
    """
    gets high score from save info (save.txt)
    score should be formatted as: h_score={HIGH SCORE}
    """
    
    if not os.path.exists('save.txt'):
        return None
    
    with open('save.txt', 'r') as save:
        for line in save:
            if 'h_score=' in line:
                data = line.split('=')
                return data[1] if not in_int else int(data[1])
        return None
                
state = GameState.IDLE
reset = False #used to make certain events on gamestate change repeat or not

timer = 0 #NOTE timer is aggregate of deltatime used to count towards one tick
ticks = 0 #NOTE 1 tick == 0.5 second

high_score = get_highscore(in_int=True)

score = 0 #current score (base is 0)
score_incr = 10 #amt score given per score tick
score_ticks = 2 #amt of ticks before score tick
score_ticks_t = score_ticks #temp current tick goal for score incr

m_bronze_score = 0 
m_silver_score = 300
m_gold_score = 600
m_plat_score = 900

base_speed = 500
speed = base_speed #current speed
speed_incr = 60 #speed increased per speed tick
speed_ticks = 15 #amt of ticks before speed tick
speed_ticks_t = speed_ticks #temp current tick goal for speed incr