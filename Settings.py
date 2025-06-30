import pygame

# Game Size
columns = 10
rows= 20
cell_size = 40 # Size of each cell
game_width, game_height = columns * cell_size, rows * cell_size # Calculate the game width and height

# Side Bar Size
sidebar_width = 200 # Width of the side bar
preview_height_fraction = 0.7 # Height of the preview
score_height_fraction = 1 - preview_height_fraction # Height of the score

# Window
padding = 20 # Padding between the side bar and the game
window_width = game_width + sidebar_width + padding * 3 # Calculate the window width
window_height = game_height + padding * 2 # Calculate the window height

# Game Behavior
update_start_speed = 400 # In milliseconds
move_wait_time = 200 # ms
rotate_wait_time = 200 # In milliseconds
block_offset = pygame.Vector2(columns // 2,-1) # Vector2 object; used to offset the blocks; blocks will be postioned above the grid

# Colors
yellow = '#f1e60d'
red = '#e51b20'
blue = '#204b9b'
green = '#65b32e'
purple = '#7b217f'
cyan = '#6cc6d9'
orange = '#f07e13'
gray = '#1C1C1C'
line_color = '#FFFFFF'

# Shapes
tetrominos = {
  'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': purple}, # T-Shape
  'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': yellow}, # O-Shape
  'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': blue}, # J-Shape
  'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': orange}, # L-Shape
  'I': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': cyan}, # I-Shape
  'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': green}, # S-Shape
  'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': red} # Z-Shape
}

score_data = {1: 40, 2: 100, 3: 300, 4: 1200} # dicitonary of score data

# Power-ups
power_up_types = {
    'slow_time': 'Slow Time',
    'clear_line': 'Clear Line', 
    'bomb': 'Bomb'
}

power_up_colors = {
    'slow_time': (0, 255, 255),    # Cyan
    'clear_line': (255, 255, 0),   # Yellow
    'bomb': (255, 100, 0)          # Orange
}

power_up_duration = 600  # 10 seconds at 60 FPS
