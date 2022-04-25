from pygame import Surface
from pygame.font import Font
from pygame.mixer import Sound
from utils import ImportImage

player: Surface
police: Surface
car_g: Surface
car_o: Surface
car_r: Surface
car_y: Surface
road: Surface
shadow: Surface
logo: Surface
game_over: Surface
panel: Surface
new_best: Surface
m_bronze: Surface
m_silver: Surface
m_gold: Surface
m_plat: Surface
m_shadow: Surface
spider: Surface

font: Font
font_s: Font
font_xs: Font

p_switch: Sound
p_crash: Sound
s_peek: Sound
s_attack: Sound
s_hide: Sound

def load() -> None:
    """
    Loads all assets. Call this after Pygame has been initialized!
    """

    global player, police, car_g, car_o, car_r, car_y, road, shadow, logo, game_over, panel,new_best, m_bronze, m_silver, m_gold, m_plat, m_shadow, spider
    global p_switch, p_crash, s_peek, s_attack, s_hide
    global font, font_s, font_xs

    player = ImportImage('assets/player.png', 3)
    police = ImportImage('assets/police.png', 3)
    car_g = ImportImage('assets/car_g.png', 3)
    car_o = ImportImage('assets/car_o.png', 3)
    car_r = ImportImage('assets/car_r.png', 3)
    car_y = ImportImage('assets/car_y.png', 3)
    road = ImportImage('assets/road.png', 4)
    shadow = ImportImage('assets/shadow.png', 3)
    logo = ImportImage('assets/logo.png')
    game_over = ImportImage('assets/game_over.png')
    panel = ImportImage('assets/panel.png')
    new_best = ImportImage('assets/new_best.png')
    m_bronze = ImportImage('assets/m_bronze.png', 2)
    m_silver = ImportImage('assets/m_silver.png', 2)
    m_gold = ImportImage('assets/m_gold.png', 2)
    m_plat = ImportImage('assets/m_plat.png', 2)
    m_shadow = ImportImage('assets/m_shadow.png', 2)
    spider = ImportImage('assets/spider.png', 5)

    p_switch = Sound('assets/switch.wav')
    p_crash = Sound('assets/crash.wav')
    s_peek = Sound('assets/peek.wav')
    s_attack = Sound('assets/attack.wav')
    s_hide = Sound('assets/hide.wav')
    
    font = Font('assets/font.ttf', 32)
    font_s = Font('assets/font.ttf', 16)
    font_xs = Font('assets/font.ttf', 8)

    m_shadow.set_alpha(50)
    shadow.set_alpha(50)