from settings import *
from os.path import join # os.path is a library for working with paths
import pygame

class Score:
  def __init__(self): # Initialize the score
    self.surface = pygame.Surface((sidebar_width, game_height * score_height_fraction - padding)) # Create a surface
    self.rect = self.surface.get_rect(bottomright = (window_width - padding, window_height - padding)) # Get the rect of the surface
    self.display_surface = pygame.display.get_surface() # Get the display surface

    # font
    self.font = pygame.font.Font(join('Graphics','Russo_One.ttf'), 30)

    # increment
    self.increment_height = self.surface.get_height() / 3

    # data 
    self.score = 0
    self.level = 1
    self.lines = 0

  def display_text(self, pos, text):
    text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white') # Render the text surface
    text_rext = text_surface.get_rect(center = pos) # Get the rect of the text surface
    self.surface.blit(text_surface, text_rext) # Blit the text surface onto the surface

  def run(self):
    for i, text in enumerate([('Score',self.score), ('Level', self.level), ('Lines', self.lines)]): # Loop through the data; i returns the index and text returns the value; enumarate returns the index and value
      x = self.surface.get_width() / 2 # Calculate the x position of the text
      y = self.increment_height / 2 + i * self.increment_height # Calculate the y position of the text by adding the increment height to the index
      self.display_text((x,y), text) # Display the text
    
    self.display_surface.blit(self.surface, self.rect) # Blit the surface onto the score surface; Blit stands for Block Image Transfer
    pygame.draw.rect(self.display_surface, line_color, self.rect, 2, 2)
