# Star Fighter

This is a vertically scrolling space themed shmup (or Shoot'em up) that I am creating using the Pygame module in Python. This is the first game I ever made and the first program I've written of this size and scope. I am continuously changing and adding to this game as I learn more.

To play Star Fighter you must have Python and Pygame installed.

## Controls
* **WASD** or **Arrow Keys** to move
* **Spacebar** to shoot
* Hold **F** key to move twice as fast
* **ALT + ENTER** to toggle full screen
* **ESC** to pause

## Refactoring
* Add timer class, remove this responsibility from GameManager
* Include a [state manager class](https://www.youtube.com/watch?v=j9yMFG3D7fg) to manage game_active status. Figure out how to integrate this with the game manager class

## Issues
* Player ship sprite can still move and shoot lasers upon death
* Explosion animation sprites are not transparent?

## Future Changes and Additions
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

## Asset Changes to Make:
* Replace Galaga ship with original player sprite
* Replace Space Invaders with original enemy sprites
* Replace placeholder music with original music

## Misc Notes
* Use `channel_#.play(music, -1)` to loop instead?
* Try [pygame.mixer.music](https://www.pygame.org/docs/ref/music.html) instead of the sound class for music, gives more control like queue music.