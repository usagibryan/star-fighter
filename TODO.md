### Issues That Need to be Fixed
* Player ship sprite can still move and shoot lasers briefly after death
* Windows flags exe made with Pyinstaller as a virus... [try this.](https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184)
* Using joystick module laser only fires sometimes.
* Using joystick module program crashes if controller not plugged in.

### Ideas for Future Changes and Additions
* Add twin laser powerup
* Display sprites of aliens on screen with how many points they are worth
* Allow player to enter initials if they get the high score
* Figure out how to use increasing score to increase rate of alien and laser spawn
* Show controls in game (create images with WASD, Spacebar and arrow keys, etc)
* Menu and options
* Add volume bar
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