import pygame

# Sprite class based on pygame's Sprite class
class Sprite(pygame.sprite.Sprite):
  def __init__(self, pos, surf, groups):
    super().__init__(groups)  # Initialize the base class with the sprite groups
    self.image = surf  # Surface for the sprite image
    self.rect = self.image.get_rect(topleft = pos)  # Rectangle for the sprite's position and size
    # Inflate the hitbox vertically, reducing its height by a third
    self.hitbox = self.rect.inflate(0, -self.rect.height / 3)
