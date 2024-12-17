import pygame
import random
from settings import *

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,color1,color2):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color = color1
        self.image = pygame.Surface((4,20))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = SCREEN_HEIGHT

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        if self.color == self.color1:
            self.color = self.color2
        else:
            self.color = self.color1
        self.image.fill(self.color)
        self.destroy()

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,audio):
        super().__init__()
        self.image = pygame.image.load('graphics/player_ship.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,0.15)
        self.rect = self.image.get_rect(center = (pos)) # make pos = 400,500?
        self.speed = 2
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600 # lower numbers = faster rate of fire

        self.lasers = pygame.sprite.Group()

        self.audio = audio

    def joystick_move(self,x_speed,y_speed):
        self.rect.move_ip(x_speed,y_speed)

    def get_input(self):
        # Keyboard input
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.rect.y -= self.speed
            if (keys[pygame.K_f]):
                self.rect.y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.rect.y += self.speed
            if (keys[pygame.K_f]):
                self.rect.y += self.speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x -= self.speed
            if (keys[pygame.K_f]):
                self.rect.x -= self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x += self.speed
            if (keys[pygame.K_f]):
                self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.audio.channel_3.play(self.audio.laser_sound)

        # # USB controller input
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        # # Method to move via joystick, movement is VERY SLOW for some reason
        # # x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
        # y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
        # self.joystick_move(x_speed,y_speed)
        
        for event in pygame.event.get():
            # # This method is even worse, much slower and you have to tap the stick
            if event.type == pygame.JOYAXISMOTION:
			# print(event)
			# Axis 1 (Vertical movement) controls paddle
                if event.axis == 1:  # Vertical axis on most joysticks
                    if event.value < -0.1:  # Push up
                        self.rect.y -= self.speed
                    elif event.value > 0.1:  # Push down
                        self.rect.y += self.speed
                    # else:  # Stick is centered
                    #     self.rect.y = 0
            
            # Laser is poorly responsive
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0) and self.ready: # A button shoots the laser
                    self.shoot_laser()
                    self.ready = False
                    self.laser_time = pygame.time.get_ticks()
                    self.audio.channel_3.play(self.audio.laser_sound)

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot_laser(self):
        # Single Laser
        self.lasers.add(Laser(self.rect.center,-8,'cyan','white'))

        # Twin Lasers
        # self.lasers.add(Laser(((self.rect.center[0] - 12),self.rect.center[1]),-8,'cyan','white'))
        # self.lasers.add(Laser(((self.rect.center[0] + 12),self.rect.center[1]),-8,'cyan','white'))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,screen_width,screen_height):
        super().__init__()
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        x_pos  = random.randint(20,self.screen_width - 20)
        file_path = 'graphics/' + self.color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center = (x_pos,random.randint(-300,-100)))

        # Yellow aliens zigzag
        self.yellow_zigzag_direction = random.choice([-1,1]) # 1 for right, -1 for left
        self.yellow_zigzag_counter = 0 

        # Blue aliens zigzag
        self.blue_zigzag_direction = random.choice([-1,1]) # 1 for right, -1 for left

        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        elif color == 'yellow': self.value = 300
        else: self.value = 500

    def destroy(self):
        if self.rect.y >= self.screen_height + 50: # added 50 to give the score time to decrease
            self.kill()

    # numbers round down if decimals are used? .05 doesn't move and 1 is the same as 1.5, etc
    def update(self):
        if self.color == 'red': self.rect.y += 1
        elif self.color == 'green': self.rect.y += 2
        elif self.color == 'yellow':
            self.rect.y += 3
            self.yellow_zigzag_counter += 1
            if self.yellow_zigzag_counter >= 100: # change direction every 100 updates
                self.yellow_zigzag_counter = 0
                self.yellow_zigzag_direction *= -1
            self.rect.x += self.yellow_zigzag_direction * 2
            if self.rect.left < 0 or self.rect.right > self.screen_width:
                self.yellow_zigzag_direction *= -1
        else: # color is blue
            self.rect.y += 5
            self.rect.x += self.blue_zigzag_direction * 2
            if self.rect.left < 0 or self.rect.right > self.screen_width:
                self.blue_zigzag_direction *= -1
        self.destroy()