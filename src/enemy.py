import pygame
from pygame.math import Vector2 as vector

from entity import Entity

class Monster:
  def get_player_distance_direction(self):
    # Calculate and return the distance and direction between the enemy and the player.
    enemy_pos = vector(self.rect.center)  # Convert the enemy's center coordinates into a vector.
    player_pos = vector(self.player.rect.center)  # Convert the player's center coordinates into a vector.
    distance = (player_pos - enemy_pos).magnitude()  # Calculate the distance between the player and the enemy.

    if distance != 0:
      direction = (player_pos - enemy_pos).normalize()  # If the distance isn't zero, calculate and normalize the direction.
    else:
      direction = vector()  # If the distance is zero, set the direction as a zero vector.

    return (distance, direction)

  def face_player(self):
    # Make the monster face the player.
    distance, direction = self.get_player_distance_direction()  # Get the distance and direction to the player.

    if distance < self.notice_radius:
      # If the player is within the monster's notice radius, update the monster's status based on the player's relative position.
      if -0.5 < direction.y < 0.5:
        if direction.x < 0:
          self.status = 'left_idle'
        elif direction.x > 0:
          self.status = 'right_idle'
      else:
        if direction.y < 0:
          self.status = 'up_idle'
        elif direction.y > 0:
          self.status = 'down_idle'

  def walk_to_player(self):
    # Make the monster walk towards the player.
    distance, direction = self.get_player_distance_direction()  # Get the distance and direction to the player.
    if self.attack_radius < distance < self.walk_radius:
      # If the player is within a certain range, the monster starts moving towards the player.
      self.direction = direction
      self.status = self.status.split('_')[0]
    else:
      self.direction = vector()  # If the player is not in range, the monster stops moving.

class Coffin(Entity, Monster):
  def __init__(self, pos, groups, path, collision_sprites, player):
    super().__init__(pos, groups, path, collision_sprites)
    self.speed = 150  # Set coffin's speed

    self.player = player  # Reference to the player object
    self.notice_radius = 550  # Radius in which the coffin starts noticing the player
    self.walk_radius = 400  # Radius in which the coffin starts walking towards the player
    self.attack_radius = 50  # Radius in which the coffin starts attacking the player

  def attack(self):
    # Define coffin's attack behavior
    distance = self.get_player_distance_direction()[0]  # Distance to player
    if distance < self.attack_radius and not self.attacking:
      self.attacking = True
      self.frame_index = 0

    if self.attacking:
      self.status = self.status.split('_')[0] + '_attack'  # Change coffin's status to attacking

  def animate(self, dt):
    # Define coffin's animation behavior
    current_animation = self.animations[self.status]

    if int(self.frame_index) == 4 and self.attacking:
      if self.get_player_distance_direction()[0] < self.attack_radius:
        self.player.damage()  # If in attack radius, player takes damage

    self.frame_index += 7 * dt
    if self.frame_index >= len(current_animation):
      self.frame_index = 0
      if self.attacking:
        self.attacking = False  # Stop attacking once the animation cycle is over

    self.image = current_animation[int(self.frame_index)]
    self.mask = pygame.mask.from_surface(self.image)

  def update(self, dt):
    # Update function to call all behavior and animation methods each frame
    self.face_player()
    self.walk_to_player()
    self.attack()
    self.move(dt)
    self.animate(dt)
    self.blink()

    self.check_death()
    self.vulnerability_timer()

class Cactus(Entity, Monster):
  def __init__(self, pos, groups, path, collision_sprites, player, create_bullet):
    super().__init__(pos, groups, path, collision_sprites)
    self.speed = 90  # Set cactus's speed

    self.player = player  # Reference to the player object
    self.notice_radius = 600  # Radius in which the cactus starts noticing the player
    self.walk_radius = 500  # Radius in which the cactus starts walking towards the player
    self.attack_radius = 350  # Radius in which the cactus starts attacking the player

    self.create_bullet = create_bullet  # Function to create a bullet
    self.bullet_shot = False  # State of whether a bullet has been shot

  def attack(self):
    # Define cactus's attack behavior
    distance = self.get_player_distance_direction()[0]  # Distance to player
    if distance < self.attack_radius and not self.attacking:
      self.attacking = True
      self.frame_index = 0
      self.bullet_shot = False

    if self.attacking:
      self.status = self.status.split('_')[0] + '_attack'  # Change cactus's status to attacking

  def animate(self, dt):
    # Define cactus's animation behavior
    current_animation = self.animations[self.status]

    if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot:
      direction = self.get_player_distance_direction()[1]  # Get direction to player
      pos = self.rect.center + direction * 150  # Calculate bullet position
      self.create_bullet(pos, direction)  # Create bullet
      self.bullet_shot = True
      self.shoot_sound.play()  # Play shooting sound

    self.frame_index += 7 * dt
    if self.frame_index >= len(current_animation):
      self.frame_index = 0
      if self.attacking:
        self.attacking = False  # Stop attacking once the animation cycle is over

    self.image = current_animation[int(self.frame_index)]
    self.mask = pygame.mask.from_surface(self.image)

  def update(self, dt):
    # Update function to call all behavior and animation methods each frame
    self.face_player()
    self.walk_to_player()
    self.attack()
    self.move(dt)
    self.animate(dt)
    self.blink()

    self.check_death()
    self.vulnerability_timer()
