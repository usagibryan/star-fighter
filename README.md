# Star Fighter <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/player_ship.png" height="32">

This is a vertically scrolling space themed shmup (or Shoot'em up) that I am creating using the Pygame module in Python. This is the first game I ever made and the first program I've written of this size and scope. I am continuously changing and adding to this game as I learn more.

To play Star Fighter you must have [Python](https://www.python.org/) and [Pygame](https://www.pygame.org/) installed.

I started learning Pygame using [Clear Code's Tutorials](https://www.youtube.com/@ClearCode) and strongly recommend starting with [The ultimate introduction to Pygame](https://www.youtube.com/watch?v=AY9MnQ4x3zk) if you are interested in learning how to make games in Pygame.

## How to Play 
Your ship starts at the center of the screen. You can move in four directions and fire upwards. There is a short cooldown timer between each shot so aim carefully. You have three hearts and if you get hit by a laser or crash into an alien ship you will take damage and lose these hearts. If you lose three hearts it's game over and your score is reset. Try to get the high score.

### Controls
* **WASD** or **Arrow Keys** to move
* **Spacebar** to shoot laser
* Hold **F** key to move twice as fast
* **ALT + ENTER** to toggle full screen
* **ESC** to pause

### Enemy Aliens
Each alien sprite behaves differently and is worth a different score value based on color:
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/red.png" width="20" height="16"> Slow - **100 Points**
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/green.png" width="20" height="16"> Moderate Speed - **200 Points**
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/yellow.png" width="20" height="16"> Fast - Moves in a Zigzag Pattern - **300 Points**
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/blue.png" width="20" height="10"> Very Fast and Rare - **500 Points**

### Assets
* "Space Invader" sprites and CRT graphics by [Clear Code](https://opengameart.org/content/assets-for-a-space-invader-like-game)
* Player ship sprite from [Top-Down Spaceships](https://opengameart.org/content/top-down-spaceships) by arin48
* Heart sprite from Undertale by Toby Fox

## Personal Notes

### Issues That Need to be Fixed
* Player ship sprite can still move and shoot lasers briefly after death
* Explosion animation sprites are not transparent?
* Windows flags exe made with Pyinstaller as a virus... [try this.](https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184)
* Using joystick module laser only fires sometimes.
* Using joystick module program crashes if controller not plugged in.

### Ideas for Future Changes and Additions
* Add twin laser powerup
* Display sprites of aliens on screen with how many points they are worth
* Allow player to enter initials if they get the high score
* Figure out how to use increasing score to increase rate of alien and laser spawn
* Show controls in game (create images with WASD, Spacebar and arrow keys, etc)
* Menu and options, allow player to change volume and difficulty
* Get extra hearts, maybe items that float down or reward for high score?
* Quit game option
* Enemy animations
* Bosses?
* Multiple levels/stages?
* Speed boost that uses energy?

### Refactoring Changes to Make
* Add timer class, remove this responsibility from GameManager
* Include a [state manager class](https://www.youtube.com/watch?v=j9yMFG3D7fg) to manage game_active status. Figure out how to integrate this with the game manager class

### Asset Changes to Make
* Replace player and enemy sprites with original art
* Replace placeholder music with original music

### Misc Notes
* Use `channel_#.play(music, -1)` to loop instead?
* Try [pygame.mixer.music](https://www.pygame.org/docs/ref/music.html) instead of the sound class for music, gives more control like queue music.