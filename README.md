# Star Fighter <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/player_ship.png" height="32">

This is a vertically scrolling space themed shmup (or Shoot'em up) that I am creating using the Pygame module in Python. This is the first game I ever made and the first program I've written of this size and scope. I am continuously changing and adding to this game as I learn more.

To play Star Fighter you must have [Python](https://www.python.org/) and [Pygame](https://www.pygame.org/) installed.

I started learning Pygame using [Clear Code's Tutorials](https://www.youtube.com/@ClearCode) and strongly recommend starting with [The ultimate introduction to Pygame](https://www.youtube.com/watch?v=AY9MnQ4x3zk) if you are interested in learning how to make games in Pygame.

## How to Play 
Your ship starts at the center of the screen. You can move in four directions and fire upwards. There is a short cooldown timer between each shot so aim carefully. You have three hearts and if you get hit by a laser or crash into an alien ship you will take damage and lose these hearts. If you lose three hearts it's game over and your score is reset. Try to get the high score.

### Controls
* **WASD** or **Arrow Keys** moves the player ship
* **Spacebar** fires the laser
* Hold **F** key to move twice as fast
* **ALT + ENTER** toggles full screen mode
* **ESC** pauses and unpauses the game
* **+** and **-** keys increase and decrease the volume

### Enemy Aliens
Each alien sprite behaves differently and is worth a different score value based on color:
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/red.png" width="20" height="16"> Slow - **100 Points**
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/green.png" width="20" height="16"> Moderate Speed - **200 Points**
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/yellow.png" width="20" height="16"> Fast - Moves in a Zigzag Pattern - **300 Points**
* <img src="https://github.com/usagibryan/star_fighter/blob/main/graphics/blue.png" width="20" height="10"> Very Fast and Rare - **500 Points**

Test