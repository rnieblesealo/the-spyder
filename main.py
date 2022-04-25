import pygame
import sys

import game_manager as gm

from enum import Enum

#TODO fix player class & spider class reassigning asset to actual instance of class :o

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('The Spyder')

# --- Asset Importing --- 

# --- Secondary Initialization ----

# --- Lanes & Obstacle Spawns ---

# --- Input Definitions --- 

# --- UI ---

# --- Road ---

# --- Obstacles ---

# --- Spider --- 

# --- Player ---

# GAME LOOP ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#temp, delete || move later


while True:
    #pygame opening
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    DELTA_TIME = CLOCK.tick() / 1000
    DISPLAY.fill((0, 0, 0))
    
    #draw road
    road_rect_a.center = road_pos_a
    road_rect_b.center = road_pos_b
    
    #move road if game not over
    if state != GameState.GAME_OVER:
        road_vel = speed
        
        road_pos_a.y += road_vel * DELTA_TIME
        road_pos_b.y += road_vel * DELTA_TIME
    
    if road_rect_a.y >= DISPLAY_SIZE[1]:
        road_pos_a.y -= road_dsp

    if road_rect_b.y >= DISPLAY_SIZE[1]:
        road_pos_b.y -= road_dsp

    DISPLAY.blit(road, road_rect_a)
    DISPLAY.blit(road, road_rect_b)

    if state != GameState.GAME_OVER:
        #if game is not over update player and spider
        player.update()
        spider.update()
        

    #always draw obstacles in obstacles list
    for obstacle in obstacles:
        obstacle.draw()
    
    #always draw player and spider
    player.draw()
    spider.draw()

    if state == GameState.IDLE:
        if len(obstacles) != 0:
            obstacles.clear()

        #draw logo
        logo_rect = logo.get_rect()
        logo_rect.center = (DISPLAY_SIZE[0] / 2, 150)
        
        #reset spider, TODO happens only once
        spider.reset()

        DISPLAY.blit(logo, logo_rect)

        #show highscore if we have one
        if high_score != None:
            hs_text = font_s.render('High Score: {H}'.format(H=high_score), False, (197, 197, 197))
            hs_text_rect = hs_text.get_rect()
            hs_text_rect.center = (DISPLAY_SIZE[0] / 2, 310)

            DISPLAY.blit(hs_text, hs_text_rect)

    if state == GameState.GAME_ON:
        #allow game values to be reset again
        if reset:
            reset = False
        
        #update obstacles
        for obstacle in obstacles:
            obstacle.update()
        
        #update score txt
        s_text = str(score)

        #remake score txt graphic if score txt changed
        if s_text != s_last_text:
            s_last_text = s_text

            #make score txt
            st = font.render(s_text, False, (255, 255, 255))

            #make score txt outline
            st_outl = font.render(s_text, False, (25, 25, 25))
            
            #maek score txt rect
            st_rect = st.get_rect()
            st_rect.center = (DISPLAY_SIZE[0] / 2, 65)
            st_pos = st_rect.topleft
        
        #draw score txt outline
        DISPLAY.blit(st_outl, (st_pos[0] - st_outl_width, st_pos[1]))
        DISPLAY.blit(st_outl, (st_pos[0] + st_outl_width, st_pos[1]))
        DISPLAY.blit(st_outl, (st_pos[0], st_pos[1] - st_outl_width))
        DISPLAY.blit(st_outl, (st_pos[0], st_pos[1] + st_outl_width))

        #draw score txt
        DISPLAY.blit(st, st_rect)
    
        #update ticks
        if timer < 0.5:
            timer += DELTA_TIME

        else:
            ticks += 1
            timer = 0

        #spawn obstacles
        if ticks == spawn_ticks_t:
            instantiate_obstacle()
            spawn_ticks_t += spawn_ticks

        #give score
        if ticks == score_ticks_t:
            score += score_incr
            score_ticks_t += score_ticks

        #speed up road
        if ticks == speed_ticks_t:
            speed += speed_incr
            speed_ticks_t += speed_ticks
        
        #trigger spider
        if ticks == spider_ticks_t:
            spider_ticks_t = spider_time()

    if state == GameState.GAME_OVER:
        #only once on game over...
        if not reset:
            #update panel
            game_over_panel.set()
            
            #reset values
            ticks = 0
            score = 0
            speed = base_speed
            spawn_ticks_t = spawn_ticks
            score_ticks_t = score_ticks
            speed_ticks_t = speed_ticks
            spider_ticks_t = spider_spawn_ticks

            reset = True
        
        #draw game over
        go_rect = game_over.get_rect()
        go_rect.center = (DISPLAY_SIZE[0] / 2, 150)
        
        #draw game over panel
        game_over_panel.draw()
        DISPLAY.blit(game_over, go_rect)

        #get restart input
        if pygame.key.get_pressed()[pygame.K_r]:
            state = GameState.IDLE

    #pygame closing
    pygame.display.update()