import pygame
import random

class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,speed,color,screen_height):
		super().__init__()
		self.image = pygame.Surface((4,20))
		self.color = color
		self.image.fill(self.color)
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = screen_height

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,x_constraint,y_constraint,speed):
		super().__init__()
		self.image = pygame.image.load('graphics/player_ship.png').convert_alpha()
		self.image = pygame.transform.rotozoom(self.image,0,2.5)
		self.rect = self.image.get_rect(center = (pos)) # make pos = 400,500?
		self.speed = speed
		self.max_x_constraint = x_constraint
		self.max_y_constraint = y_constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 600 # lower numbers = faster rate of fire

		self.lasers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.2)
		self.channel_3 = pygame.mixer.Channel(3)

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
			# self.laser_sound.play()
			if not self.channel_3.get_busy():
					self.channel_3.play(self.laser_sound)

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

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,screen_width,screen_height):
		super().__init__()
		self.color = color
		self.screen_width = screen_width
		self.screen_height = screen_height
		x_pos  = random.randint(20,self.screen_width - 20)
		file_path = 'graphics/' + self.color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(center = (x_pos,random.randint(-300,-100)))

		# Yellow aliens zigzag
		self.direction = 1 # 1 for right, -1 for left
		self.counter = 0 

		if color == 'red': self.value = 100
		elif color == 'green': self.value = 200
		else: self.value = 300

	def destroy(self):
		if self.rect.y >= self.screen_height + 50: # added 50 to give the score time to decrease
			self.kill()

	# numbers round down if decimals are used? .05 doesn't move and 1 is the same as 1.5, etc
	def update(self):
		if self.color == 'red': self.rect.y += 1
		elif self.color == 'green': self.rect.y += 3
		else: # color is yellow
			self.rect.y += 3
			self.counter += 1
			if self.counter >= 100: # change direction every 100 updates
				self.counter = 0
				self.direction *= -1
			self.rect.x += self.direction * 2
			if self.rect.left < 0 or self.rect.right > self.screen_width:
				self.direction *= -1
		self.destroy()