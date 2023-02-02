import pygame
from settings import *

pygame.init()
font = pygame.font.Font(None,30)

def debug(info,y = SCREEN_HEIGHT - 20,x = 10):
	display_surf = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surf,'Black',debug_rect)
	display_surf.blit(debug_surf,debug_rect)