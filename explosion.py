import pygame, sys

class Explosion(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.is_animating = False
		self.sprites = []
		self.sprites.append(pygame.image.load('../graphics/attack_1.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_2.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_3.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_4.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_5.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_6.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_7.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_8.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_9.png'))
		self.sprites.append(pygame.image.load('../graphics/attack_10.png'))
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x,pos_y] # center this?

	def explode(self):
		self.is_animating = True

	def update(self,speed):
		if self.is_animating == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.kill()
			else:
				self.image = self.sprites[int(self.current_sprite)]