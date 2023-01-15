"""
GOALS:

- add music
- add sounds
- add scrolling background
- add unique start and game overscreens
- add scoring system
- add shooting mechanic
- kill enemy sprites on shoot collide
- re-work using code structure from Space Invaders tutorial (clean classes across mutliple files)
"""

import pygame, sys, random
from laser import Laser

class Crosshair(pygame.sprite.Sprite):
	def __init__(self,picture_path):
		super().__init__()
		self.image = pygame.image.load(picture_path)
		self.rect = self.image.get_rect()
		self.gunshot = pygame.mixer.Sound("audio/laser.wav")
	def shoot(self):
		self.gunshot.play()
		pygame.sprite.spritecollide(crosshair,obstacle_group,True)
	def update(self):
		self.rect.center = pygame.mouse.get_pos()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('graphics/player_ship.png').convert_alpha()
		self.image = pygame.transform.rotozoom(self.image,0,2.5)
		self.rect = self.image.get_rect(center = (400,500))

		self.lasers = pygame.sprite.Group()

	def player_input(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top >= 0:
			self.rect.y -= 5
			if (keys[pygame.K_TAB]):
				self.rect.y -= 5
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom <= screen_height:
			self.rect.y += 5
			if (keys[pygame.K_TAB]):
				self.rect.y += 5
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left >= 0:
			self.rect.x -= 5
			if (keys[pygame.K_TAB]):
				self.rect.x -= 5
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right <= screen_width:
			self.rect.x += 5
			if (keys[pygame.K_TAB]):
				self.rect.x += 5

		if keys[pygame.K_SPACE]:
			self.shoot_laser()

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

	def update(self):
		self.player_input()
		self.lasers.update()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'boss_galaga':
			boss_galaga_1 = pygame.image.load('graphics/boss_galaga_1.png').convert_alpha()
			boss_galaga_1 = pygame.transform.rotozoom(boss_galaga_1,0,2.5)
			boss_galaga_2 = pygame.image.load('graphics/boss_galaga_2.png').convert_alpha()
			boss_galaga_2 = pygame.transform.rotozoom(boss_galaga_2,0,2.5)
			self.frames = [boss_galaga_1,boss_galaga_2]
			x_pos = random.randint(0,screen_width)
		else:
			zako_1 = pygame.image.load('graphics/zako_1.png').convert_alpha()
			zako_1 = pygame.transform.rotozoom(zako_1,0,2.5)
			zako_2 = pygame.image.load('graphics/zako_2.png').convert_alpha()
			zako_2 = pygame.transform.rotozoom(zako_2,0,2.5)
			self.frames = [zako_1,zako_2]
			x_pos  = random.randint(0,screen_width)

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (x_pos,random.randint(-300,-100)))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.y += 6
		self.destroy()

	def destroy(self):
		if self.rect.y >= screen_height: 
			self.kill()

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

def game_messages():
	welcome_message = basic_font.render(f'Rail Shooter',False,(font_color))
	welcome_message_rect = welcome_message.get_rect(center = (screen_width/2,screen_height/2 - 50))
	start_message = basic_font.render(f'Press Space to Begin ',False,(font_color))
	start_message_rect = start_message.get_rect(center = (screen_width/2,screen_height/2 + 50))
	game_over_message = basic_font.render(f'Game Over',False,(font_color))
	game_over_message_rect = game_over_message.get_rect(center = (screen_width/2,screen_height/2 - 50))
	continue_message = basic_font.render(f'Press Space to Continue ',False,(font_color))
	continue_message_rect = continue_message.get_rect(center = (screen_width/2,screen_height/2 + 50))

	if game_start == True:
		screen.blit(welcome_message,welcome_message_rect)
		screen.blit(start_message, start_message_rect)
	else:
		screen.blit(game_over_message,game_over_message_rect)
		screen.blit(continue_message, continue_message_rect)

pygame.init()

# Main Window
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED)
pygame.display.set_caption('Rail Shooter')
clock = pygame.time.Clock()

# Variables
game_active = False
game_start = True

# Colors
bg_color = pygame.Color('grey12')
font_color = pygame.Color('White')

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Crosshair
crosshair = Crosshair("graphics/crosshair.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Text
basic_font = pygame.font.Font("freesansbold.ttf",32)

# Sound

# Music
bg_music = pygame.mixer.Sound('audio/corneria.mp3')
#bg_music.set_volume(0.5)
channel = pygame.mixer.Channel(0)
#death_sound = pygame.mixer.Sound('audio/arwing_crash.mp3')
#death_sound.set_volume(0.5)

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,200) # lower numbers = faster rate of enemy spawn

# Main Game Loop
while True:
	
	# Handling Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			crosshair.shoot()	
		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(random.choice(['boss_galaga','zako','zako','zako'])))
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True

		if event.type == pygame.KEYDOWN:
			if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
				pygame.display.toggle_fullscreen()

	# Visuals & Game Logic
	screen.fill(bg_color)

	if game_active:
		if not channel.get_busy():
			channel.play(bg_music) # play forever. (bg_music, -1)

		player.draw(screen)
		player.sprite.lasers.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		pygame.draw.line(screen,'Red',player.sprite.rect.center,pygame.mouse.get_pos())

		crosshair_group.draw(screen)
		crosshair_group.update()

		game_active = collision_sprite()
		game_start = False
	else:
		game_messages()

	# Updating the window
	pygame.display.flip()
	clock.tick(60)