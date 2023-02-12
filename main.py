import pygame
import sys, random, time
import json
from settings import *
from animations import Background, Explosion, CRT
from sprites import Laser, Player, Alien
from style import Style
from audio import Audio
import debug

class GameManager:
	def __init__(self):

		# Game setup
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED)
		pygame.display.set_caption('Star Fighter')
		self.clock = pygame.time.Clock()
		self.game_active = False
		self.style = Style(self.screen)
		self.crt = CRT(self.screen)
		self.audio = Audio()
		self.paused = False

		# Player Health
		self.hearts = 3
		self.heart_surf = pygame.image.load('graphics/undertale_heart.png').convert_alpha()
		self.heart_x_start_pos = SCREEN_WIDTH - (self.heart_surf.get_size()[0] * 3 + 30)

		# Background Setup
		self.background = pygame.sprite.Group()
		Background(self.background)

		# Player setup
		player_sprite = Player((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
		self.player = pygame.sprite.GroupSingle(player_sprite)
		self.player_alive = True

		# Score setup
		self.score = 0
		self.save_data = {
			'high_score' : 0
		}

		try:
			with open('high_score.txt') as high_score_file:
				self.save_data = json.load(high_score_file)
		except:
			print('No file created yet')

		# Timers
		self.alien_spawn_rate = 600 # lower numbers = faster rate of enemy spawn
		self.alien_spawn_timer = pygame.event.custom_type()
		pygame.time.set_timer(self.alien_spawn_timer,self.alien_spawn_rate)

		self.alien_laser_rate = 400 # lower numbers = more lasers
		self.alien_laser_timer = pygame.event.custom_type()
		pygame.time.set_timer(self.alien_laser_timer,self.alien_laser_rate)

		self.player_death_timer = pygame.event.custom_type()

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()

		# Explosion setup
		self.exploding_sprites = pygame.sprite.Group()

		# Audio setup
		self.play_intro_music = True # Set to False after user begins, only place once

	def spawn_aliens(self,alien_color):
		self.aliens.add(Alien(alien_color,SCREEN_WIDTH,SCREEN_HEIGHT))
		if alien_color == 'blue':
			self.audio.channel_5.play(self.audio.ufo_sound) # causes the game to lag

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = random.choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,4,'yellow','white') # 2nd arg is alien laser speed
			self.alien_lasers.add(laser_sprite)

	def explode(self,x_pos,y_pos):
		self.audio.channel_2.play(self.audio.explosion_sound)
		self.explosion = Explosion(x_pos,y_pos)
		self.exploding_sprites.add(self.explosion)
		self.explosion.explode()

	def collision_checks(self):
		# when the player shoots an alien
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					laser.kill()
					self.explode(alien.rect.x - 25,alien.rect.y - 25) # why isn't this centered?

		# when an alien shoots the player
		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.hearts -= 1
					if self.hearts == 2:
						self.audio.channel_4.play(self.audio.low_health_alarm1)
					if self.hearts == 1:
						self.audio.channel_4.play(self.audio.low_health_alarm2)
					if self.hearts <= 0:
						self.explode(self.player.sprite.rect.x - 25,self.player.sprite.rect.y - 25)
						self.audio.channel_1.pause()
						self.player_alive = False
						pygame.time.set_timer(self.player_death_timer,500)

		# when an alien and the player collide
		aliens_crash = pygame.sprite.spritecollide(self.player.sprite,self.aliens,True)
		if aliens_crash:
			for alien in aliens_crash:
				self.score += alien.value
				if self.hearts > 1:
					self.explode(alien.rect.x - 25,alien.rect.y - 25)
			self.hearts -= 1
			if self.hearts == 2:
				self.audio.channel_4.play(self.audio.low_health_alarm1)
			if self.hearts == 1:
				self.audio.channel_4.play(self.audio.low_health_alarm2)
			if self.hearts <= 0:
				self.explode(self.player.sprite.rect.x - 25,self.player.sprite.rect.y - 25)
				self.audio.channel_1.pause()
				self.player_alive = False
				pygame.time.set_timer(self.player_death_timer,500)

	def score_check(self):
		if self.score > self.save_data['high_score']:
			self.save_data['high_score'] = self.score

	def display_hearts(self):
		for heart in range(self.hearts):
			x = self.heart_x_start_pos + (heart * (self.heart_surf.get_size()[0] + 10))
			self.screen.blit(self.heart_surf,(x,8))

	def pause(self):
		self.paused = not self.paused
		while self.paused:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					with open('high_score.txt','w') as high_score_file:
						json.dump(self.save_data,high_score_file)
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
						pygame.display.toggle_fullscreen()
					if event.key == pygame.K_ESCAPE:
						self.audio.channel_0.unpause()
						self.audio.channel_1.unpause()
						self.audio.channel_7.play(self.audio.unpause_sound)
						self.paused = False
			self.screen.fill((0, 0, 0))
			self.style.update('pause',self.save_data,self.score)
			pygame.display.update()

	def run(self):
		last_time = time.time()
		while True:
			print(self.audio.master_volume)
			dt = time.time() - last_time
			last_time = time.time()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					with open('high_score.txt','w') as high_score_file:
						json.dump(self.save_data,high_score_file)
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
						pygame.display.toggle_fullscreen()
					if event.key == pygame.K_ESCAPE:
						self.audio.channel_0.pause()
						self.audio.channel_1.pause()
						self.audio.channel_6.play(self.audio.pause_sound)
						self.pause()
					if event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
						self.audio.master_volume += 0.1
						self.audio.master_volume = min(self.audio.master_volume, 1.0)
						self.audio.update()
					elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
						self.audio.master_volume -= 0.1
						self.audio.master_volume = max(self.audio.master_volume, 0.0)
						self.audio.update()
				if self.game_active:
					if event.type == self.alien_spawn_timer:
						alien_color = random.choice(['red','red','red','red','red',
													 'green','green','green',
													 'yellow','yellow',
													 'blue'])
						self.spawn_aliens(alien_color)
					if event.type == self.alien_laser_timer:
						self.alien_shoot()
					if event.type == self.player_death_timer:
						self.audio.player_down.play()
						self.aliens.empty()
						self.game_active = False
						pygame.time.set_timer(self.player_death_timer,0)
				else:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.score = 0
						self.player.sprite.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
						self.hearts = 3
						self.alien_lasers.empty()
						self.player_alive = True
						self.game_active = True

			self.screen.fill((30,30,30))
			self.background.update(dt)
			self.background.draw(self.screen)

			if self.game_active:
				self.audio.channel_0.stop()
				self.play_intro_music = False
				if not self.audio.channel_1.get_busy():
					self.audio.channel_1.play(self.audio.bg_music)
				self.player.update()
				self.alien_lasers.update()

				self.aliens.update()
				self.collision_checks()
				self.display_hearts()

				self.player.sprite.lasers.draw(self.screen)
				if self.player_alive:
					self.player.draw(self.screen)
				self.exploding_sprites.draw(self.screen)
				self.exploding_sprites.update(0.15) # smaller numbers = slower explosion animation. Always 0.x
				self.aliens.draw(self.screen)
				self.alien_lasers.draw(self.screen)
				self.score_check()
				self.style.update('game_active',self.save_data,self.score)
			else:
				self.audio.channel_1.stop()
				if self.play_intro_music == True:
					if not self.audio.channel_0.get_busy():
						self.audio.channel_0.play(self.audio.intro_music)

				if self.score == 0:
					self.style.update('intro',self.save_data,self.score)
				else:
					self.style.update('game_over',self.save_data,self.score)
				
			self.crt.draw()
			pygame.display.flip()
			self.clock.tick(FRAMERATE)

if __name__ == '__main__':
	game_manager = GameManager()
	game_manager.run()