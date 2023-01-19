"""
GOALS:

- add quit game option
- add original music
- change laser sounds (player laser and alien lasers should be different)(make alien laser sound less annoying or constant)
- add unique start and game overscreens, game_active state
- add scoring system
- collision without groupcollide?
- add music channels
- allow user to change volume in game (options menu?)
- add animations
"""

import pygame, sys, random, time
from settings import *
from player import Player
from alien import Alien
from laser import Laser
from background import BG

class Game:
	def __init__(self):

		# Game setup
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED)
		pygame.display.set_caption('Star Fighter')
		self.clock = pygame.time.Clock()

		# Timers
		self.alien_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.alien_timer,2000) # lower numbers = faster rate of enemy spawn

		self.ALIENLASER = pygame.USEREVENT + 1
		pygame.time.set_timer(self.ALIENLASER,400)

		# Background Setup
		self.background = pygame.sprite.Group()

		# scale factor
		bg_width = pygame.image.load('../graphics/background.png').get_width()
		self.scale_factor = SCREEN_WIDTH / bg_width

		BG(self.background,self.scale_factor)

		# Player setup
		player_sprite = Player((SCREEN_WIDTH/2,SCREEN_HEIGHT/2),SCREEN_WIDTH,SCREEN_HEIGHT,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# Score setup
		self.score = 0
		self.font = pygame.font.Font('../font/Pixeled.ttf',20)

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()

		# Audio
		music = pygame.mixer.Sound('../audio/corneria.mp3')
		music.set_volume(1)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.3)
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_sound.set_volume(0.5)

	def spawn_aliens(self,alien_color):
		self.aliens.add(Alien(alien_color,SCREEN_WIDTH,SCREEN_HEIGHT))

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = random.choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,3,'green',SCREEN_HEIGHT) # 2nd arg is alien laser speed
			self.alien_lasers.add(laser_sprite)
			#self.laser_sound.play() replace with quieter or less annoying sound

	def collision_checks(self):
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# why does groupcollide work but in the Space Invaders code spritecollide works with the alien group?
				# can't use score like space invaders code because group object has no attribute value?
				if pygame.sprite.groupcollide(self.player.sprite.lasers,self.aliens,False,True):
					laser.kill()
					self.explosion_sound.play()
					self.score += 1
		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser,self.player,False): # change to game over
					laser.kill()
					pygame.quit()
					sys.exit()
		if pygame.sprite.spritecollide(self.player.sprite,self.aliens,False): # game over if you touch a ship
			pygame.quit()
			sys.exit()

	# def score_drop(self):
	# 	for alien in self.aliens.sprites():
	# 		if alien.rect.bottom == SCREEN_HEIGHT:
	# 			self.score -= 1 # doesn't work every single time
			
	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-10))
		self.screen.blit(score_surf,score_rect)

	def run(self):
		last_time = time.time()
		while True:
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == self.alien_timer:
					alien_color = random.choice(['red','green','yellow'])
					game.spawn_aliens(alien_color)
				if event.type == self.ALIENLASER:
					game.alien_shoot()
				if event.type == pygame.KEYDOWN:
					if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
						pygame.display.toggle_fullscreen()

			self.screen.fill((30,30,30))
			self.background.update(dt)
			self.background.draw(self.screen)

			self.player.update()
			self.alien_lasers.update()

			self.aliens.update()
			self.collision_checks()

			self.player.sprite.lasers.draw(self.screen)
			self.player.draw(self.screen)
			self.aliens.draw(self.screen)
			self.alien_lasers.draw(self.screen)
			# self.score_drop()
			self.display_score()

			pygame.display.flip()
			self.clock.tick(FRAMERATE)

if __name__ == '__main__':
	game = Game()
	game.run()