import pygame
from settings import *

# see https://www.youtube.com/watch?v=VUFvY349ess for more details
class BG(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		bg_image = pygame.image.load('../graphics/background.png').convert()
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