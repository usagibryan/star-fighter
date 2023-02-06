import pygame
from settings import *

class Audio():
    def __init__(self):
        super().__init__()
        self.intro_music = pygame.mixer.Sound('audio/star_fox_controls.mp3')
        self.intro_music.set_volume(.5)
        self.channel_0 = pygame.mixer.Channel(0)
        self.play_intro_music = True # Set to False after user begins, only place once

        self.bg_music = pygame.mixer.Sound('audio/star_hero.mp3')
        self.bg_music.set_volume(1) # very low for some reason
        self.channel_1 = pygame.mixer.Channel(1)

        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)
        self.channel_2 = pygame.mixer.Channel(2)

        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.2)
        self.channel_3 = pygame.mixer.Channel(3)

        self.low_health_alarm1 = pygame.mixer.Sound('audio/sfx_alarm_loop2.wav')
        self.low_health_alarm1.set_volume(0.3)
        self.channel_4 = pygame.mixer.Channel(4)

        self.low_health_alarm2 = pygame.mixer.Sound('audio/sfx_alarm_loop1.wav')
        self.low_health_alarm2.set_volume(0.3)
        self.channel_5 = pygame.mixer.Channel(5)

        # game lags when this is called on blue alien spawn
        # tried in many places, and still lags even if it's not called, too many channels at this point?
        # too many audio objects created???
        # self.ufo_sound = pygame.mixer.Sound('audio/sfx_sound_bling.wav')
        # self.ufo_sound.set_volume(.03)
        # self.channel_6 = pygame.mixer.Channel(6)

        self.player_down = pygame.mixer.Sound('audio/player_down.mp3')
        self.player_down.set_volume(.5)