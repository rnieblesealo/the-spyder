import vars as v
import assets as a
import game_manager as gm

from pygame.math import Vector2

class GameOverPanel:
    medal = None #medal img to use
    is_new_best = False

    __panel_pos = Vector2(v.DISPLAY_SIZE[0] / 2, 275)
    __panel_rect = a.panel.get_rect()

    __medal_local_pos = Vector2(52, a.panel.get_height() / 2)
    __medal_rect = a.m_bronze.get_rect()

    __text_local_pos = Vector2(__medal_local_pos.x + 148, a.panel.get_height() / 2)
    __text_surf = None
    __text_rect = None

    __nbest_local_pos = Vector2(__text_local_pos.x, __text_local_pos.y + 35)
    __nbest_rect = a.new_best.get_rect()
    
    __mshadow_rect = a.m_shadow.get_rect()

    def __init__(self):
        #position
        self.__panel_rect.center = self.__panel_pos
        self.__medal_rect.center = self.__medal_local_pos #NOTE local pos refers to local position within panel rect (we blit these to their parent surface rather than the display)
        self.__mshadow_rect.center = self.__medal_local_pos

    def set(self):
        #check new best & set
        global high_score
        if high_score == None or gm.score > high_score:
            self.is_new_best = True
            self.__nbest_rect.center = self.__nbest_local_pos

            #write score
            if gm.get_highscore() == None or gm.score > gm.get_highscore(in_int=True):
                with open('save.txt', 'w+') as save:
                    save.truncate(0)
                    save.write('h_score={H}'.format(H=gm.score))
            
        #update displayed highscore to savefile one
        high_score = gm.get_highscore()
        
        #determine medal from score
        if gm.score < gm.m_silver_score:
            self.medal = gm.m_bronze
        elif gm.score < gm.m_gold_score:
            self.medal = gm.m_silver
        elif gm.score < gm.m_plat_score:
            self.medal = gm.m_gold
        else:
            self.medal = gm.m_plat

        #set text
        self.__text_surf = a.font_s.render("Score: {s}, Best: {b}".format(s = gm.score, b = high_score), False, (197, 197, 197))
        self.__text_rect = self.__text_surf.get_rect()
        self.__text_rect.center = self.__text_local_pos

    def draw(self):
        #draw panel
        v.DISPLAY.blit(a.panel, self.__panel_rect)

        #draw medal shadow
        a.panel.blit(a.m_shadow, self.__mshadow_rect)

        #draw medal        
        a.panel.blit(self.medal, self.__medal_rect)

        #draw text
        a.panel.blit(self.__text_surf, self.__text_rect)

        #draw new best if applies
        if self.is_new_best:
            a.panel.blit(a.new_best, self.__nbest_rect)


game_over_panel = GameOverPanel() #TODO move to main.py

#Score Text, Fix Later

# s_text = str(score)
# s_last_text = None

# st_outl_width = 5

# st: Surface = None
# st_outl: Surface = None
# st_rect: Rect = None