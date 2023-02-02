import pygame
import sys, random, time
import json
from settings import *
from animations import BG, Explosion, CRT
from sprites import Laser, Player, Alien
import debug

class GameManager:
	def __init__(self):

		# Game setup
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED)
		pygame.display.set_caption('Star Fighter')
		self.clock = pygame.time.Clock()
		self.game_active = False
		self.font = pygame.font.Font('font/Pixeled.ttf',20)
		self.font_color = 'white'
		self.crt = CRT(self.screen)
		self.paused = False

		# Intro screen
		self.player_ship = pygame.image.load('graphics/player_ship.png').convert_alpha()
		self.player_ship = pygame.transform.rotozoom(self.player_ship,0,5)
		self.player_ship_rect = self.player_ship.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

		self.game_name = self.font.render('STAR FIGHTER',False,(self.font_color))
		self.game_name_rect = self.game_name.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 100))

		self.game_message = self.font.render('PRESS ENTER TO BEGIN',False,(self.font_color))
		self.game_message_rect = self.game_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 130))

		# Health and Lives
		self.lives = 3
		self.live_surf = pygame.image.load('graphics/player_ship.png').convert_alpha()
		self.live_surf = pygame.transform.rotozoom(self.player_ship,0,0.3)
		self.live_x_start_pos = SCREEN_WIDTH - (self.live_surf.get_size()[0] * 2 + 20)

		# Background Setup
		self.background = pygame.sprite.Group()
		BG(self.background)

		# Player setup
		player_sprite = Player((SCREEN_WIDTH/2,SCREEN_HEIGHT/2),SCREEN_WIDTH,SCREEN_HEIGHT,2)
		self.player = pygame.sprite.GroupSingle(player_sprite)

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
		self.alien_spawn_rate = 800 # lower numbers = faster rate of enemy spawn
		self.alien_spawn_timer = pygame.event.custom_type()
		pygame.time.set_timer(self.alien_spawn_timer,self.alien_spawn_rate - int(self.score / 10))

		self.alien_laser_rate = 400 # lower numbers = more lasers
		self.alien_laser_timer = pygame.event.custom_type()
		pygame.time.set_timer(self.alien_laser_timer,self.alien_laser_rate - int(self.score / 10))

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()

		# Explosion setup
		self.exploding_sprites = pygame.sprite.Group()

		# Audio
		self.intro_music = pygame.mixer.Sound('audio/star_fox_controls.mp3')
		self.intro_music.set_volume(1)
		self.channel_0 = pygame.mixer.Channel(0)
		self.play_intro_music = True # Set to False after user begins, only place once
		
		self.bg_music = pygame.mixer.Sound('audio/corneria.mp3')
		self.bg_music.set_volume(1)
		self.channel_1 = pygame.mixer.Channel(1)
		
		# self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		# self.laser_sound.set_volume(0.5)

		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)
		self.channel_2 = pygame.mixer.Channel(2)

		self.player_down = pygame.mixer.Sound('audio/player_down.mp3')
		self.player_down.set_volume(1) # play faster?

	def spawn_aliens(self,alien_color):
		self.aliens.add(Alien(alien_color,SCREEN_WIDTH,SCREEN_HEIGHT))

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = random.choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,4,'green',SCREEN_HEIGHT) # 2nd arg is alien laser speed
			self.alien_lasers.add(laser_sprite)
			#self.laser_sound.play() replace with quieter or less annoying sound

	def explode(self,x_pos,y_pos):
		if not self.channel_2.get_busy():
			self.channel_2.play(self.explosion_sound)
		# self.explosion_sound.play()
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
					self.lives -= 1
					self.explode(self.player.sprite.rect.x - 25,self.player.sprite.rect.y - 25)
					if self.lives <= 0:
						self.player_down.play()
						self.aliens.empty()
						self.game_active = False

		# when an alien and the player collide
		aliens_crash = pygame.sprite.spritecollide(self.player.sprite,self.aliens,True)
		if aliens_crash:
			for alien in aliens_crash:
				self.score += alien.value
			self.lives -= 1
			self.explode(self.player.sprite.rect.x - 25,self.player.sprite.rect.y - 25)
			if self.lives <= 0:
				self.player_down.play()
				self.aliens.empty()
				self.game_active = False

	def score_check(self):
		if self.score > self.save_data['high_score']:
			self.save_data['high_score'] = self.score
			
	def display_score(self):
		high_score_surf = pygame.font.Font('font/Pixeled.ttf',10).render(f'HIGH SCORE: {self.save_data["high_score"]}',False,self.font_color)
		high_score_rect = high_score_surf.get_rect(topleft = (10,5))
		self.screen.blit(high_score_surf,high_score_rect)

		score_surf = self.font.render(f'SCORE: {self.score}',False,self.font_color)
		score_rect = score_surf.get_rect(topleft = (10,20))
		self.screen.blit(score_surf,score_rect)

	def display_lives(self):
		for live in range(self.lives - 1):
			x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
			self.screen.blit(self.live_surf,(x,8))

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
						self.paused = False
			self.screen.fill((0, 0, 0))
			pause_text = self.font.render('PAUSED', False, (self.font_color))
			pause_text_rect = pause_text.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
			self.screen.blit(pause_text,pause_text_rect)
			pygame.display.update()

	def run(self):
		last_time = time.time()
		while True:
			# print(str(self.clock.get_fps())) # use debug to print this?
			# delta time (scrolling background breaks without delta time?)
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
						self.pause()
				if self.game_active:
					if event.type == self.alien_spawn_timer:
						alien_color = random.choice(['red','green','yellow'])
						self.spawn_aliens(alien_color)
					if event.type == self.alien_laser_timer:
						self.alien_shoot()
				else:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.score = 0
						self.player.sprite.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
						self.lives = 3
						self.game_active = True

			self.screen.fill((30,30,30))
			self.background.update(dt)
			self.background.draw(self.screen)

			if self.game_active:
				self.channel_0.stop()
				self.play_intro_music = False
				if not self.channel_1.get_busy():
					self.channel_1.play(self.bg_music)
				self.player.update()
				self.alien_lasers.update()

				self.aliens.update()
				self.collision_checks()
				self.display_lives()

				self.player.sprite.lasers.draw(self.screen)
				self.player.draw(self.screen)
				self.exploding_sprites.draw(self.screen)
				self.exploding_sprites.update(0.15) # smaller numbers = slower explosion animation. Always 0.x
				self.aliens.draw(self.screen)
				self.alien_lasers.draw(self.screen)
				self.score_check()
				self.display_score()
				# debug.debug(self.alien_spawn_rate)
			else:
				self.channel_1.stop()
				if self.play_intro_music == True:
					if not self.channel_0.get_busy():
						self.channel_0.play(self.intro_music)
				self.screen.blit(self.player_ship,self.player_ship_rect)


				high_score_message = self.font.render(f'HIGH SCORE: {self.save_data["high_score"]}',False,(self.font_color))
				high_score_message_rect = high_score_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 100))
				score_message = self.font.render(f'YOUR SCORE: {self.score}',False,(self.font_color))
				score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 130))
				self.screen.blit(self.game_name,self.game_name_rect)

				if self.score == 0:
					self.screen.blit(high_score_message,high_score_message_rect)
					self.screen.blit(self.game_message,self.game_message_rect)
				else:
					self.screen.blit(high_score_message,high_score_message_rect)
					self.screen.blit(score_message,score_message_rect)
				
			self.crt.draw()
			pygame.display.flip()
			self.clock.tick(FRAMERATE)

if __name__ == '__main__':
	game_manager = GameManager()
	game_manager.run()
