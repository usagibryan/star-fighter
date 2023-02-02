import pygame
import random
from settings import *

# see https://www.youtube.com/watch?v=VUFvY349ess for more details
class BG(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		bg_image = pygame.image.load('graphics/background.png').convert()
		full_height = bg_image.get_height()
		full_width = bg_image.get_width()
		self.image = pygame.Surface((full_width,full_height * 2))

		self.image.blit(bg_image,(0,0))
		self.image.blit(bg_image,(0,full_height))

		self.rect = self.image.get_rect(bottomleft = (0,SCREEN_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.bottomleft)

	def update(self,dt):
		self.pos.y += 300 * dt # Scrolling background breaks without delta time formula?
		if self.rect.top >= 0:
			self.pos.y = -self.image.get_height() / 2
		self.rect.y = round(self.pos.y) # Understand this before you can simplify it

class Explosion(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.is_animating = False
		
		# sprite sheet from https://www.pngwing.com/en/free-png-xiyem/
		sprite_sheet = pygame.image.load('graphics/explosion.png').convert_alpha()

		self.sprites = []
		self.sprites.append(self.get_image(sprite_sheet,0,192,192,.5))
		self.sprites.append(self.get_image(sprite_sheet,1,192,192,.5))
		self.sprites.append(self.get_image(sprite_sheet,2,192,192,.5))
		self.sprites.append(self.get_image(sprite_sheet,3,192,192,.5))
		self.sprites.append(self.get_image(sprite_sheet,4,192,192,.5))
		self.sprites.append(self.get_image(sprite_sheet,5,192,192,.5))
		self.sprites.append(self.get_image(sprite_sheet,6,192,192,.5))

		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x,pos_y] # center this?

	# see sprite sheet tutorials by Coding With Russ:
	# https://www.youtube.com/watch?v=M6e3_8LHc7A
	# https://www.youtube.com/watch?v=M6e3_8LHc7A 
	def get_image(self, sheet, frame, width ,height, scale):
		surf = pygame.Surface((width,height)).convert_alpha()
		surf.blit(sheet,(0,0),((frame*width),0,width,height))
		surf = pygame.transform.scale(surf, (width * scale, height * scale))
		return surf

	def explode(self):
		self.is_animating = True

	def update(self, speed):
		if self.is_animating == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.kill()
			else:
				self.image = self.sprites[int(self.current_sprite)]

class CRT:
	def __init__(self,screen):
		super().__init__()
		self.screen = screen
		self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(SCREEN_WIDTH,SCREEN_HEIGHT))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(SCREEN_HEIGHT / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,'black',(0,y_pos),(SCREEN_WIDTH,y_pos),1)

	def draw(self):
		self.tv.set_alpha(random.randint(75,90))
		self.create_crt_lines()
		self.screen.blit(self.tv,(0,0))