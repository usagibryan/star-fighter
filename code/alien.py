import pygame
import random

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,screen_width,screen_height):
		super().__init__()
		self.screen_width = screen_width
		self.screen_height = screen_height
		x_pos  = random.randint(0,self.screen_width)
		file_path = '../graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(center = (x_pos,random.randint(-300,-100)))

	def destroy(self):
		if self.rect.y >= self.screen_height: 
			self.kill()

	def update(self):
		self.rect.y += 6
		self.destroy()
