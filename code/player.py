import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,x_constraint,y_constraint,speed):
		super().__init__()
		self.image = pygame.image.load('../graphics/player_ship.png').convert_alpha()
		self.image = pygame.transform.rotozoom(self.image,0,2.5)
		self.rect = self.image.get_rect(center = (pos)) # make pos = 400,500?
		self.speed = speed
		self.max_x_constraint = x_constraint
		self.max_y_constraint = y_constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 300

		self.lasers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)

	def get_input(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_w] or keys[pygame.K_UP]):
			self.rect.y -= self.speed
			if (keys[pygame.K_TAB]):
				self.rect.y -= self.speed
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
			self.rect.y += self.speed
			if (keys[pygame.K_TAB]):
				self.rect.y += self.speed
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
			self.rect.x -= self.speed
			if (keys[pygame.K_TAB]):
				self.rect.x -= self.speed
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
			self.rect.x += self.speed
			if (keys[pygame.K_TAB]):
				self.rect.x += self.speed

		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= self.max_y_constraint:
			self.rect.bottom = self.max_y_constraint

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center,-8,'red',self.rect.bottom))

	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()