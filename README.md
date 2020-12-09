# APP 
Another Platformer Project
  
15-112 Fall 2020 Term Project


A very difficult platformer based off I Wanna Be the Guy, and other similar platformers
Try to push through the difficult stages, and even the occasional boss battle. Navigate
the platfoms with pixel perfect accruacy, dodge traps, fight off bosses, and get
as far as possible!
Remember, a single hit is death, so make use of loading and saving!

# HOW TO RUN
Simply run python game.py, or run game.py in a linter.

# HOW TO PLAY
W and D move left and right. Space causes the player to jump. The player can double jump, with
their double jump refreshed on the ground.
Enter shoots a projectile. They dissipate on contact with a tile, and when an enemy is hit
the projectile deals 1 damage.
Shooting a save block will save the player's state and stage. Pressing R (whether alive or dead)
will return the player to that location and that stage. Use this if you're stuck!
Stages are randomly generated, and each stage has a possible path to get to the end.
Traps are also randomly generated, including a dart trap, spikes, disappearing tiles, moving
platforms, lasers, et cetera. The number and the difficulty of the traps increase as the game continues
The boss fight occurs every 15 stages. The boss has to be shot at until its HP is reduced to 0, shown
at the top of the screen. The attacks of the boss are displayed at the bottom.
The attacks of the boss change depending on what was last used, and what the player is doing. Take care to not
do the same thing too many times, or the boss will start adjusting!
The boss also enrages when below a certain threshold. When the boss's HP is reduced to 0, tiles appear to offer a path
to the next level.
Try to get as far as you can before the stages get too difficult!

Additional keys described in debugging and shortcut commands.


# LIBRARIES NEEDED
pygame
cmu_112_graphics.py

# DEBUGGING AND SHORTCUT COMMANDS
P will pause the game
X will move the game one tick forward when paused
G toggles invincibility
B toggles showing bounding boxes in green