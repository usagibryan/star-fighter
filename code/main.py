import pygame, sys, random
from player import Player
from alien import Alien
from laser import Laser

class Game:
	def __init__(self):
		# Player setup
		player_sprite = Player((screen_width/2,screen_height/2),screen_width,screen_height,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# Alien setup
		#self.aliens = pygame.sprite.Group()

		# Audio
		music = pygame.mixer.Sound('../audio/corneria.mp3')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)

	# def alien_setup():
	# 	for event in events:
	# 		if event.type == alien_timer:
	# 				alien_color = random.choice(['red','green','yellow'])
	# 				aliens.add(Alien(alien_color,screen_width,screen_height))

#	def collision_checks(self):

	def run(self):
		self.player.update()

		#self.aliens.update()
		#self.collision_checks()

		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		#self.aliens.draw(screen)

if __name__ == '__main__':
	pygame.init()
	screen_width = 600
	screen_height = 800
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()

	# Alien setup (ry to put this in the Game class)
	aliens = pygame.sprite.Group()

	# Timer 
	alien_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(alien_timer,200) # lower numbers = faster rate of enemy spawn


	# Multiple event loops? Or same event loop in class and main loop?
	#events = pygame.event.get():

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == alien_timer:
				alien_color = random.choice(['red','green','yellow'])
				aliens.add(Alien(alien_color,screen_width,screen_height))

		screen.fill((30,30,30))
		game.run()

		aliens.draw(screen)
		aliens.update()
			
		pygame.display.flip()
		clock.tick(60)