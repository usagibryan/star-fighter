"""
GOALS:

- add music
- add sounds
- add original pixel art
- add scrolling background
- add unique start and game overscreens
- add scoring system
- add shooting mechanic
"""

import pygame, sys, random

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('graphics/player_ship.png').convert_alpha()
		self.image = pygame.transform.rotozoom(self.image,0,2.5)
		self.rect = self.image.get_rect(center = (400,500))

	def player_input(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top >= 0:
			self.rect.y -= 5
			if (keys[pygame.K_SPACE]):
				self.rect.y -= 5
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom <= 600:
			self.rect.y += 5
			if (keys[pygame.K_SPACE]):
				self.rect.y += 5
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left >= 0:
			self.rect.x -= 5
			if (keys[pygame.K_SPACE]):
				self.rect.x -= 5
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right <= 800:
			self.rect.x += 5
			if (keys[pygame.K_SPACE]):
				self.rect.x += 5

	def update(self):
		self.player_input()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'boss_galaga':
			boss_galaga_1 = pygame.image.load('graphics/boss_galaga_1.png').convert_alpha()
			boss_galaga_1 = pygame.transform.rotozoom(boss_galaga_1,0,2.5)
			boss_galaga_2 = pygame.image.load('graphics/boss_galaga_2.png').convert_alpha()
			boss_galaga_2 = pygame.transform.rotozoom(boss_galaga_2,0,2.5)
			self.frames = [boss_galaga_1,boss_galaga_2]
			x_pos = random.randint(0,600)
		else:
			zako_1 = pygame.image.load('graphics/zako_1.png').convert_alpha()
			zako_1 = pygame.transform.rotozoom(zako_1,0,2.5)
			zako_2 = pygame.image.load('graphics/zako_2.png').convert_alpha()
			zako_2 = pygame.transform.rotozoom(zako_2,0,2.5)
			self.frames = [zako_1,zako_2]
			x_pos  = random.randint(0,600)

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
		if self.rect.y >= 600: 
			self.kill()

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

pygame.init()

# Main Window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Rail Shooter')
clock = pygame.time.Clock()

# Variables
game_active = False

# Colors
bg_color = pygame.Color('grey12')
font_color = pygame.Color('White')

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Text
basic_font = pygame.font.Font("freesansbold.ttf",32)

# Sound

# Music

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
		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(random.choice(['boss_galaga','zako','zako','zako'])))
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True

	# Visuals & Game Logic
	screen.fill(bg_color)

	if game_active:

		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
	else:
		game_over_message = basic_font.render(f'Game Over',False,(font_color))
		game_over_message_rect = game_over_message.get_rect(center = (400,250))
		continue_message = basic_font.render(f'Press Space to Continue ',False,(font_color))
		continue_message_rect = continue_message.get_rect(center = (400,350))
		screen.blit(game_over_message,game_over_message_rect)
		screen.blit(continue_message, continue_message_rect)

	# Updating the window
	pygame.display.flip()
	clock.tick(60)