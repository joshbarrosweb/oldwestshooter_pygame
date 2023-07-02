import pygame, sys
from pytmx.util_pygame import load_pygame

from pygame.math import Vector2 as vector
from settings import *
from player import Player
from sprite import Sprite
from bullet import Bullet
from enemy import Coffin, Cactus

# Custom group class to handle drawing sprites with an offset and background image
class AllSprites(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    self.offset = vector()  # Offset to be applied when drawing sprites
    self.display_surface = pygame.display.get_surface()  # Display surface to draw onto
    self.bg = pygame.image.load('./resources/graphics/other/bg.png').convert()  # Background image

  def customize_draw(self, player):
    # Method to draw sprites with offset according to player position and with background
    self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
    self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

    self.display_surface.blit(self.bg, -self.offset)  # Draw background with offset

    # Draw all sprites with offset sorted by their y-coordinate
    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
      offset_rect = sprite.image.get_rect(center = sprite.rect.center)
      offset_rect.center -= self.offset
      self.display_surface.blit(sprite.image, offset_rect)

class Game:
  def __init__(self):
    pygame.init()  # Initialize pygame
    pygame.display.set_caption('Old West Rampage')  # Set window title
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Set up display surface
    self.clock = pygame.time.Clock()  # Set up clock for frame rate control
    self.bullet_surf = pygame.image.load('./resources/graphics/other/particle.png').convert_alpha()  # Load bullet image

    # Set up sprite groups
    self.all_sprites = AllSprites()
    self.obstacles = pygame.sprite.Group()
    self.bullets = pygame.sprite.Group()
    self.monsters = pygame.sprite.Group()

    self.setup()  # Set up the game

    # Load and play background music
    self.music = pygame.mixer.Sound('./resources/sound/music.mp3')
    self.music.play(loops = -1)

  def create_bullet(self, pos, direction):
    # Create a new bullet
    Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])

  def bullet_collision(self):
    # Handle bullet collisions
    for obstacle in self.obstacles.sprites():
      pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask)

    for bullet in self.bullets.sprites():
      sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)

      if sprites:
        bullet.kill()
        for sprite in sprites:
          sprite.damage()

    if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
      self.player.damage()

  def setup(self):
    # Set up the game world using a tmx map
    tmx_map = load_pygame('./resources/data/map.tmx')
    for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
      Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])

    for obj in tmx_map.get_layer_by_name('Objects'):
      Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

    for obj in tmx_map.get_layer_by_name('Entities'):
      if obj.name == 'Player':
        self.player = Player(
          pos = (obj.x, obj.y),
          groups = self.all_sprites,
          path = PATHS['player'],
          collision_sprites = self.obstacles,
          create_bullet = self.create_bullet
        )

      if obj.name == 'Coffin':
        Coffin((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['coffin'], self.obstacles, self.player)

      if obj.name == 'Cactus':
        Cactus((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['cactus'], self.obstacles, self.player, self.create_bullet)

  def run(self):
    # Game loop
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      dt = self.clock.tick() / 1000  # Get time since last frame

      self.all_sprites.update(dt)  # Update all sprites
      self.bullet_collision()  # Check for bullet collisions

      self.display_surface.fill('black')  # Clear the display surface
      self.all_sprites.customize_draw(self.player)  # Draw all sprites

      pygame.display.update()  # Update the display

if __name__ == '__main__':
  game = Game()  # Create a new game
  game.run()  # Run the game
