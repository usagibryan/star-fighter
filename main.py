import pygame, sys, random, time
from settings import *
from player import Player
from alien import Alien
from laser import Laser
from background import BG
from crt import CRT
from explosion import Explosion

class Game:
	def __init__(self):

		# Game setup
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED)
		pygame.display.set_caption('Star Fighter')
		self.clock = pygame.time.Clock()
		self.game_active = False
		self.font = pygame.font.Font('../font/Pixeled.ttf',20)
		self.font_color = ('white')
		self.crt = CRT(self.screen)

		# Intro screen
		self.player_ship = pygame.image.load('../graphics/player_ship.png').convert_alpha()
		self.player_ship = pygame.transform.rotozoom(self.player_ship,0,5)
		self.player_ship_rect = self.player_ship.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

		self.game_name = self.font.render('STAR FIGHTER',False,(self.font_color))
		self.game_name_rect = self.game_name.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 100))

		self.game_message = self.font.render('PRESS SPACE TO BEGIN',False,(self.font_color))
		self.game_message_rect = self.game_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 100))

		# Timers
		self.alien_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.alien_timer,2000) # lower numbers = faster rate of enemy spawn

		self.ALIENLASER = pygame.USEREVENT + 1
		pygame.time.set_timer(self.ALIENLASER,400)

		# Background Setup
		self.background = pygame.sprite.Group()
		BG(self.background)

		# Player setup
		player_sprite = Player((SCREEN_WIDTH/2,SCREEN_HEIGHT/2),SCREEN_WIDTH,SCREEN_HEIGHT,2)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# Score setup
		self.score = 0

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()

		# Explosion setup
		self.exploding_sprites = pygame.sprite.Group()

		# Audio
		music = pygame.mixer.Sound('../audio/brinstar.mp3')
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
			laser_sprite = Laser(random_alien.rect.center,4,'green',SCREEN_HEIGHT) # 2nd arg is alien laser speed
			self.alien_lasers.add(laser_sprite)
			#self.laser_sound.play() replace with quieter or less annoying sound

	def collision_checks(self):
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					laser.kill()
					self.explosion_sound.play()
					self.explosion = Explosion(alien.rect.x,alien.rect.y)
					self.exploding_sprites.add(self.explosion)
					self.explosion.explode()

		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser,self.player,False): # change to game over
					laser.kill()
					self.aliens.empty()
					self.game_active = False
		if pygame.sprite.spritecollide(self.player.sprite,self.aliens,False): # game over if you touch a ship
			self.aliens.empty()
			self.game_active = False
			
	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-10))
		self.screen.blit(score_surf,score_rect)

	def run(self):
		last_time = time.time()
		while True:
			# delta time (scrolling background breaks without delta time?)
			dt = time.time() - last_time
			last_time = time.time()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
						pygame.display.toggle_fullscreen()
				if self.game_active:
					if event.type == self.alien_timer:
						alien_color = random.choice(['red','green','yellow'])
						game.spawn_aliens(alien_color)
					if event.type == self.ALIENLASER:
						game.alien_shoot()
				else:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						self.score = 0
						self.game_active = True

			self.screen.fill((30,30,30))
			self.background.update(dt)
			self.background.draw(self.screen)

			if self.game_active:
				self.player.update()
				self.alien_lasers.update()

				self.aliens.update()
				self.collision_checks()

				self.player.sprite.lasers.draw(self.screen)
				self.player.draw(self.screen)
				self.aliens.draw(self.screen)
				self.alien_lasers.draw(self.screen)
				self.exploding_sprites.draw(self.screen)
				self.exploding_sprites.update(0.25)
				self.display_score()
			else:
				self.screen.blit(self.player_ship,self.player_ship_rect)

				score_message = self.font.render(f'YOUR SCORE: {self.score}',False,(self.font_color))
				score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 100))
				self.screen.blit(self.game_name,self.game_name_rect)

				if self.score == 0: self.screen.blit(self.game_message,self.game_message_rect)
				else: self.screen.blit(score_message,score_message_rect)
				
			self.crt.draw()
			pygame.display.flip()
			self.clock.tick(FRAMERATE)

if __name__ == '__main__':
	game = Game()
	game.run()