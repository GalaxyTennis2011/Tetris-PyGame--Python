from settings import *
from sys import exit
from os.path import join
import os

# Set SDL video driver for Replit compatibility
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# components
from game import Game
from score import Score
from preview import Preview
from rules import Rules

from random import choice

class Main:
  def __init__(self):

    # general 
    pygame.init()
    self.display_surface = pygame.display.set_mode((window_width,window_height))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Tetris')

    # shapes
    self.next_shapes = [choice(list(tetrominos.keys())) for shape in range(3)]

    # components
    self.game = Game(self.get_next_shape, self.update_score)
    self.score = Score()
    self.preview = Preview()
    self.rules = Rules()

    # audio 
    self.music = pygame.mixer.Sound(join('Sound','music.wav'))
    self.music.set_volume(0.05)
    self.music.play(-1)

  def update_score(self, lines, score, level):
    self.score.lines = lines
    self.score.score = score
    self.score.level = level

  def get_next_shape(self):
    next_shape = self.next_shapes.pop(0)
    self.next_shapes.append(choice(list(tetrominos.keys())))
    return next_shape

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_r:
            self.rules.toggle()

      # display 
      self.display_surface.fill(gray)

      # components (only run game if rules not showing)
      if not self.rules.showing:
        self.game.run()
        self.score.run()
        self.preview.run(self.next_shapes)

      # Always run rules (it handles its own visibility)
      self.rules.run()

      # updating the game
      pygame.display.update()
      self.clock.tick(60)  # Set to 60 FPS for smoother gameplay

if __name__ == '__main__':
  main = Main()
  main.run()
