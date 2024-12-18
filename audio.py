import pygame
from settings import *

class Audio():
    def __init__(self):
        super().__init__()
        self.master_volume = 0.5 # default value is 1.0

        """Music"""
        self.intro_music = pygame.mixer.Sound('audio/star_fighter_intro.ogg')
        self.intro_music.set_volume(self.master_volume * 2) # Low volume for some reason
        self.channel_0 = pygame.mixer.Channel(0)
        self.play_intro_music = True # Set to False after user begins, only plays once

        self.bg_music = pygame.mixer.Sound('audio/star_hero.mp3')
        self.bg_music.set_volume(self.master_volume)
        self.channel_1 = pygame.mixer.Channel(1)

        # Not tied to a channel?
        self.player_down = pygame.mixer.Sound('audio/game_over.ogg')
        self.player_down.set_volume(self.master_volume)

        """
        Sound Effects
        Divide by 2 on initialize and update as they are too loud compared to the music
        """
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(self.master_volume / 2)
        self.channel_3 = pygame.mixer.Channel(3)
        
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(self.master_volume / 2)
        self.channel_2 = pygame.mixer.Channel(2)

        # Low Health Alarms share channel
        self.low_health_alarm1 = pygame.mixer.Sound('audio/sfx_alarm_loop2.wav')
        self.low_health_alarm1.set_volume(self.master_volume / 2)
        self.low_health_alarm2 = pygame.mixer.Sound('audio/sfx_alarm_loop1.wav')
        self.low_health_alarm2.set_volume(self.master_volume / 2)
        self.channel_4 = pygame.mixer.Channel(4)

        self.ufo_sound = pygame.mixer.Sound('audio/sfx_sound_bling.wav')
        self.ufo_sound.set_volume(self.master_volume / 2)
        self.channel_5 = pygame.mixer.Channel(5)

        self.pause_sound = pygame.mixer.Sound('audio/sfx_sounds_pause2_in.wav')
        self.pause_sound.set_volume(self.master_volume / 2)
        self.channel_6 = pygame.mixer.Channel(6)

        self.unpause_sound = pygame.mixer.Sound('audio/sfx_sounds_pause2_out.wav')
        self.unpause_sound.set_volume(self.master_volume / 2)
        self.channel_7 = pygame.mixer.Channel(7)

    def update(self):
        """Updates volume of all sounds and music"""
        self.intro_music.set_volume(self.master_volume)
        self.bg_music.set_volume(self.master_volume)
        self.player_down.set_volume(self.master_volume)
        self.laser_sound.set_volume(self.master_volume / 2)
        self.explosion_sound.set_volume(self.master_volume / 2)
        self.low_health_alarm1.set_volume(self.master_volume / 2)
        self.low_health_alarm2.set_volume(self.master_volume / 2)
        self.ufo_sound.set_volume(self.master_volume / 2)
        self.pause_sound.set_volume(self.master_volume / 2)
        self.unpause_sound.set_volume(self.master_volume / 2)