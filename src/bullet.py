import pygame

class Bullet(pygame.sprite.Sprite):
  # Bullet class inherits from the Sprite class in Pygame.
  def __init__(self, pos, direction, surf, groups):
    # Initialize the Bullet class.
    super().__init__(groups)
    self.image = surf  # Load the bullet image.
    self.mask = pygame.mask.from_surface(self.image)  # Create a mask for the bullet image. This is used for pixel-perfect collision detection.
    self.rect = self.image.get_rect(center = pos)  # Get the rectangle object that encloses the bullet image.

    self.pos = pygame.math.Vector2(self.rect.center)  # Convert the rect center into a 2D vector.
    self.direction = direction  # Store the bullet's direction of travel.
    self.speed = 400  # Set the speed of the bullet.

  def update(self, dt):
    # This method updates the bullet's position.
    self.pos += self.direction * self.speed * dt  # Move the bullet in its direction at the set speed.
    self.rect.center = (round(self.pos.x), round(self.pos.y))  # Update the rectangle center with the new position.
