import pygame, os
from pygame.math import Vector2 as vector
from math import sin

class Entity(pygame.sprite.Sprite):
  def __init__(self, pos, groups, path, collision_sprites):
    super().__init__(groups)  # Initialize parent class

    self.import_assets(path)  # Import assets (sprites) from the specified path
    self.frame_index = 0  # Initialize the frame index for animations
    self.status = 'down'  # Set the initial status

    # Set the image of the sprite, get its rect and set its center
    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(center = pos)

    self.pos = vector(self.rect.center)  # Position vector
    self.direction = vector()  # Direction vector
    self.speed = 200  # Movement speed

    # Define hitbox and collision detection properties
    self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
    self.collision_sprites = collision_sprites  # Sprites with which this entity can collide
    self.mask = pygame.mask.from_surface(self.image)

    self.attacking = False  # State of whether entity is currently attacking

    self.health = 3  # Health points
    self.is_vulnerable = True  # State of vulnerability
    self.hit_time = None  # Timestamp when entity was hit

    # Sound effect when hit and when shooting
    self.hit_sound = pygame.mixer.Sound('./resources/sound/hit.mp3')
    self.hit_sound.set_volume(0.5)
    self.shoot_sound = pygame.mixer.Sound('./resources/sound/bullet.wav')
    self.shoot_sound.set_volume(0.5)

  def blink(self):
    # Blink effect when entity is not vulnerable
    if not self.is_vulnerable:
      if self.wave_value():
        mask = pygame.mask.from_surface(self.image)
        white_surf = mask.to_surface()
        white_surf.set_colorkey((0, 0, 0))
        self.image = white_surf

  def wave_value(self):
    # Helper function for the blink method
    value = sin(pygame.time.get_ticks())
    if value >= 0:
      return True
    else:
      return False

  def damage(self):
    # Reduce health by 1 if entity is vulnerable, play hit sound and make entity invulnerable
    if self.is_vulnerable:
      self.health -= 1
      self.is_vulnerable = False
      self.hit_time = pygame.time.get_ticks()
      self.hit_sound.play()

  def check_death(self):
    # Check if health points are 0 or less and kill entity if true
    if self.health <= 0:
      self.kill()

  def vulnerability_timer(self):
    # If entity is invulnerable, check if 400 milliseconds have passed since hit, make entity vulnerable again if true
    if not self.is_vulnerable:
      current_time = pygame.time.get_ticks()
      if current_time - self.hit_time > 400:
        self.is_vulnerable = True

  def import_assets(self, path):
    # Load all animation sprites from given path
    self.animations = {}
    for index, folder in enumerate(os.walk(path)):
      if index == 0:
        for name in folder[1]:
          self.animations[name] = []
      else:
        for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
          path = folder[0].replace(os.sep, '/') + '/' + file_name
          surf = pygame.image.load(path).convert_alpha()
          key = folder[0].split(os.sep)[5]
          self.animations[key].append(surf)

  def move(self, dt):
    # Move the entity according to its direction vector
    if self.direction.magnitude() != 0:
      self.direction = self.direction.normalize()

    # Move horizontally, check for collision
    self.pos.x += self.direction.x * self.speed * dt
    self.hitbox.centerx = round(self.pos.x)
    self.rect.centerx = self.hitbox.centerx
    self.collision('horizontal')

    # Move vertically, check for collision
    self.pos.y += self.direction.y * self.speed * dt
    self.hitbox.centery = round(self.pos.y)
    self.rect.centery = self.hitbox.centery
    self.collision('vertical')

  def collision(self, direction):
    # Check for collisions and adjust position to avoid overlapping
    for sprite in self.collision_sprites.sprites():
      if sprite.hitbox.colliderect(self.hitbox):
        if direction == 'horizontal':
          if self.direction.x > 0:
            self.hitbox.right = sprite.hitbox.left
          if self.direction.x < 0:
            self.hitbox.left = sprite.hitbox.right
          self.rect.centerx = self.hitbox.centerx
          self.pos.x = self.hitbox.centerx
        else:
          if self.direction.y > 0:
            self.hitbox.bottom = sprite.hitbox.top
          if self.direction.y < 0:
            self.hitbox.top = sprite.hitbox.bottom
          self.rect.centery = self.hitbox.centery
          self.pos.y = self.hitbox.centery
