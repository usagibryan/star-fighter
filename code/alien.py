import pygame
import random

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,screen_width,screen_height):
		super().__init__()
		self.color = color
		self.screen_width = screen_width
		self.screen_height = screen_height
		x_pos  = random.randint(10,self.screen_width - 10)
		file_path = '../graphics/' + self.color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(center = (x_pos,random.randint(-300,-100)))

		if color == 'red': self.value = 100
		elif color == 'green': self.value = 200
		else: self.value = 300

	def destroy(self):
		if self.rect.y >= self.screen_height + 50: # added 50 to give the score time to decrease
			self.kill()

	# numbers round down if decimals are used? .05 doesn't move and 1 is the same as 1.5, etc
	def update(self):
		if self.color == 'red': self.rect.y += 1
		elif self.color == 'green': self.rect.y += 2
		else: self.rect.y += 3
		self.destroy()