# Old West Rampage with Pygame

This project is a recreation of an Old West themed shooter, implemented in Python using the Pygame library.

## Special Thanks

Special thanks to all the game developers out there, for inspiring this project!

## Project Structure

The project has the following file and folder structure:

### `src`

This folder contains the source code files for the game:

- `main.py`: The main entry point of the game. It sets up the game, initiates the game loop, and manages the main game objects and logic.
- `bullet.py`: Contains the Bullet class which handles the behaviour of bullets, including their movement and collision detection.
- `enemy.py`: Contains the enemy classes (Coffin, Cactus), each defining the behaviour, animations, and logic of each enemy type.
- `entity.py`: Contains the Entity class, a base class for all game characters that handles shared characteristics like movement, animation, health, and damage.
- `player.py`: Contains the Player class which handles player character behaviour, such as movement, shooting, health tracking, and input handling.
- `settings.py`: Contains global game settings and constants, like window size, and paths to assets.
- `sprite.py`: Contains the Sprite class which is used to create static objects in the game world, like fences and obstacles.

### `resources`

This folder contains various resources used in the game:

#### `graphics`

This subfolder contains the game's graphics files, organised into folders for each type of graphic (entity, other).

#### `sound`

This subfolder contains the game's sound files, such as sound effects and background music.

#### `data`

This subfolder contains the game's map file (`map.tmx`).

## Instructions

To run the project, follow these steps:

1. Install Python 3 if you haven't already.
2. Install the Pygame and PyTMX libraries by running the command: `pip install pygame pytmx`.
3. Navigate to the project directory.
4. Run the command: `python3 src/main.py`.

Make sure you have the required resources in the appropriate directories as shown in the folder structure.

Feel free to modify and explore the game to suit your needs.

Enjoy playing!

---
