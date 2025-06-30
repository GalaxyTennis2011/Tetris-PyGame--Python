from settings import *
from pygame.image import load
from os import path
import pygame

class Preview:
  def __init__(self): # Initialize the Preview class

    # General
    self.display_surface = pygame.display.get_surface() # Get the display surface
    self.surface = pygame.Surface((sidebar_width, game_height * preview_height_fraction)) # Create a surface
    self.rect = self.surface.get_rect(topright = (window_width - padding, padding)) # Get the rect of the surface

    # Shapes
    self.shape_surfaces = {shape: load(path.join('Graphics', f'{shape}.png')).convert_alpha() for shape in tetrominos.keys()} # Load the shape graphics

    # Image position Darta
    self.increment_height = self.surface.get_height() / 3 # Calculate the fragment height for each tetromino to fit perfectly in the preview

  def display_pieces(self, shapes):
    for i, shape in enumerate(shapes): # Loop through the shapes; i returns the index and shape returns the value; enumarate returns the index and value
      shape_surface = self.shape_surfaces[shape] # Get the shape surface
      x = self.surface.get_width() / 2
      y = self.increment_height / 2 + i * self.increment_height # Calculate the y position of the shape by adding the increment height to the index
      rect = shape_surface.get_rect(center = (x, y)) # Get the rect of the shape surface
      self.surface.blit(shape_surface, rect) # Blit the shape surface onto the surface
      

  def run(self, next_shapes):
    self.surface.fill(gray) # Fill the surface with gray
    self.display_pieces(next_shapes)
    self.display_surface.blit(self.surface, self.rect) # Blit the surface onto the display surface
    pygame.draw.rect(self.display_surface, line_color, self.rect, 2, 2) # Draw a rectangle around the surface with line_color and 2 pixels
