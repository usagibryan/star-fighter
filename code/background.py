import pygame
from settings import *

# see https://www.youtube.com/watch?v=VUFvY349ess for more details
class BG(pygame.sprite.Sprite):
	def __init__(self,groups,scale_Factor):
		super().__init__(groups)
		bg_image = pygame.image.load('../graphics/background.png').convert()

		full_height = bg_image.get_height() * scale_Factor
		full_width = bg_image.get_width() * scale_Factor
		full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))

		self.image = pygame.Surface((full_width,full_height * 2))
		self.image.blit(full_sized_image,(0,0))
		self.image.blit(full_sized_image,(0,-full_height)) # not drawing?

		self.rect = self.image.get_rect(bottomleft = (0,SCREEN_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.bottomleft)

	def update(self,dt):
		self.pos.y += 300 * dt # change to += 300 to move
		if self.rect.top >= 800:
			self.pos.y = 0
		self.rect.y = round(self.pos.y)
