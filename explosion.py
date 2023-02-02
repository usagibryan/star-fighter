import pygame

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

	# see YouTube tutorial: 
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