import pygame
from random import randint
from settings import *

class CRT:
	def __init__(self,screen):
		super().__init__()
		self.screen = screen
		self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(SCREEN_WIDTH,SCREEN_HEIGHT))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(SCREEN_HEIGHT / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,'black',(0,y_pos),(SCREEN_WIDTH,y_pos),1)

	def draw(self):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		self.screen.blit(self.tv,(0,0))