import pygame, sys

from pygame.math import Vector2 as vector

from entity import Entity

# Player class derived from the Entity class
class Player(Entity):
  def __init__(self, pos, groups, path, collision_sprites, create_bullet):
    super().__init__(pos, groups, path, collision_sprites)
    self.create_bullet = create_bullet  # Function to create bullet
    self.bullet_shot = False  # Track if bullet is shot or not

  def get_status(self):
    # Update status of the player based on its direction and attacking state
    if self.direction.x == 0 and self.direction.y == 0:
      self.status = self.status.split('_')[0] + '_idle'
    if self.attacking:
      self.status = self.status.split('_')[0] + '_attack'

  def input(self):
    # Handle keyboard inputs for the player
    keys = pygame.key.get_pressed()
    if not self.attacking:
      if keys[pygame.K_RIGHT]:
        self.direction.x = 1
        self.status = 'right'
      elif keys[pygame.K_LEFT]:
        self.direction.x = -1
        self.status = 'left'
      else:
        self.direction.x = 0

      if keys[pygame.K_DOWN]:
        self.direction.y = 1
        self.status = 'down'
      elif keys[pygame.K_UP]:
        self.direction.y = -1
        self.status = 'up'
      else:
        self.direction.y = 0

      if keys[pygame.K_SPACE]:
        self.attacking = True
        self.direction = vector()
        self.frame_index = 0
        self.bullet_shot = False

        direction = self.status.split('_')[0]
        if direction == 'left':
            self.bullet_direction = vector(-1, 0)
        elif direction == 'right':
            self.bullet_direction = vector(1, 0)
        elif direction == 'up':
            self.bullet_direction = vector(0, -1)
        elif direction == 'down':
            self.bullet_direction = vector(0, 1)

  def animate(self, dt):
    # Animate the player
    current_animation = self.animations[self.status]

    self.frame_index += 7 * dt
    if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
      bullet_start_pos = self.rect.center + self.bullet_direction * 80
      self.create_bullet(bullet_start_pos, self.bullet_direction)
      self.bullet_shot = True
      self.shoot_sound.play()

    if self.frame_index >= len(current_animation):
      self.frame_index = 0
      if self.attacking:
        self.attacking = False

    self.image = current_animation[int(self.frame_index)]
    self.mask = pygame.mask.from_surface(self.image)

  def check_death(self):
    # Check if the player is dead and quit if so
    if self.health <= 0:
      pygame.quit()
      sys.exit()

  def update(self, dt):
    # Update the player
    self.input()  # Handle inputs
    self.get_status()  # Update status
    self.move(dt)  # Move player
    self.animate(dt)  # Animate player
    self.blink()  # Make player blink

    self.check_death()  # Check for player death
    self.vulnerability_timer()  # Update vulnerability timer
