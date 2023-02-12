import pygame
from settings import *

class Style():
    def __init__(self,screen,audio):
        super().__init__() # why is this necessary?
        self.screen = screen
        self.small_font = pygame.font.Font('font/Pixeled.ttf',10)
        self.medium_font = pygame.font.Font('font/Pixeled.ttf',20)
        self.large_font = pygame.font.Font('font/Pixeled.ttf',30)
        self.font_color = 'white'

        # Load image of ship for intro and game over screens
        self.player_ship = pygame.image.load('graphics/player_ship.png').convert_alpha()
        self.player_ship = pygame.transform.rotozoom(self.player_ship,0,0.2)
        self.player_ship_rect = self.player_ship.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        # Needed to display the volume
        self.audio = audio

    # Displays the title on the intro and game over screens
    def display_title(self):
        title = self.large_font.render('STAR FIGHTER',False,(self.font_color))
        title_rect = title.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 100))
        self.screen.blit(title,title_rect)

    # Displays Game Over message
    def display_game_over(self):
        game_over_message = self.large_font.render('GAME OVER',False,(self.font_color))
        game_over_message_rect = game_over_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 100))
        self.screen.blit(game_over_message,game_over_message_rect)

    def display_player_ship(self):
        self.screen.blit(self.player_ship,self.player_ship_rect)

    # Displays instructions on how to begin on the intro screen (show controls in this method?)
    def display_intro_message(self):
        intro_message = self.medium_font.render('PRESS ENTER TO BEGIN',False,(self.font_color))
        intro_message_rect = intro_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 130))
        self.screen.blit(intro_message,intro_message_rect)

    # Displays the high score on the intro and game over screens
    def display_high_score(self,save_data):
        self.save_data = save_data

        high_score_message = self.medium_font.render(f'HIGH SCORE: {self.save_data["high_score"]}',False,(self.font_color))
        high_score_message_rect = high_score_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 100))
        self.screen.blit(high_score_message,high_score_message_rect)

    # Displays the high score and current score on the top left during gameplay
    def display_in_game_score(self,save_data,score):
        self.save_data = save_data
        self.score = score

        high_score_surf = self.small_font.render(f'HIGH SCORE: {self.save_data["high_score"]}',False,self.font_color)
        high_score_rect = high_score_surf.get_rect(topleft = (10,5))
        self.screen.blit(high_score_surf,high_score_rect)

        score_surf = self.medium_font.render(f'SCORE: {self.score}',False,self.font_color)
        score_rect = score_surf.get_rect(topleft = (10,20))
        self.screen.blit(score_surf,score_rect)

    # Displays the player score on the game over screen
    def display_game_over_score(self,score):
        self.score = score

        score_message = self.medium_font.render(f'YOUR SCORE: {self.score}',False,(self.font_color))
        score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 130))
        self.screen.blit(score_message,score_message_rect)

    # Displays the Pause message on pause
    def display_pause_text(self):
        pause_text = self.medium_font.render('PAUSED', False, (self.font_color))
        pause_text_rect = pause_text.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(pause_text,pause_text_rect)

    def display_volume(self):
        volume_message = self.small_font.render(f'VOLUME: {round(self.audio.master_volume * 10)}',False,(self.font_color))
        volume_message_rect = volume_message.get_rect(bottomleft = (10,SCREEN_HEIGHT - 10))
        self.screen.blit(volume_message,volume_message_rect)

    def update(self,game_state,save_data,score):
        self.game_state = game_state
        self.save_data = save_data
        self.score = score

        if game_state == 'intro':
            self.display_title()
            self.display_high_score(self.save_data)
            self.display_intro_message()
            self.display_player_ship()
        elif game_state == 'game_active':
            self.display_in_game_score(self.save_data,self.score)
        elif game_state == 'game_over':
            self.display_game_over()
            self.display_high_score(self.save_data)
            self.display_game_over_score(self.score)
            self.display_player_ship()
        elif game_state == 'pause':
            self.display_pause_text()