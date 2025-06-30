
from settings import *
import pygame

class Rules:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((window_width, window_height))
        self.rect = self.surface.get_rect()
        
        # Font setup
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
        
        # Colors
        self.bg_color = (20, 20, 20)
        self.title_color = (255, 255, 255)
        self.header_color = (0, 255, 255)
        self.text_color = (200, 200, 200)
        self.highlight_color = (255, 255, 0)
        
        self.showing = False
        
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.surface.blit(text_surface, (x, y))
        return y + text_surface.get_height() + 5
        
    def draw_rules(self):
        self.surface.fill(self.bg_color)
        
        y = 30
        
        # Title
        y = self.draw_text("TETRIS RULES", self.title_font, self.title_color, 50, y)
        y += 20
        
        # Controls section
        y = self.draw_text("CONTROLS:", self.header_font, self.header_color, 50, y)
        y = self.draw_text("← → Arrow Keys: Move left/right", self.text_font, self.text_color, 70, y)
        y = self.draw_text("↓ Arrow Key: Fast drop", self.text_font, self.text_color, 70, y)
        y = self.draw_text("↑ Arrow Key: Rotate piece", self.text_font, self.text_color, 70, y)
        y = self.draw_text("R Key: Show/hide rules", self.text_font, self.text_color, 70, y)
        y += 20
        
        # Gameplay section
        y = self.draw_text("GAMEPLAY:", self.header_font, self.header_color, 50, y)
        y = self.draw_text("• Stack falling pieces to form complete lines", self.text_font, self.text_color, 70, y)
        y = self.draw_text("• Complete lines disappear and give points", self.text_font, self.text_color, 70, y)
        y = self.draw_text("• Game speeds up as your level increases", self.text_font, self.text_color, 70, y)
        y = self.draw_text("• Gray ghost piece shows where current piece will land", self.text_font, self.text_color, 70, y)
        y += 20
        
        # Scoring section
        y = self.draw_text("SCORING:", self.header_font, self.header_color, 50, y)
        y = self.draw_text("1 Line: 40 × Level", self.text_font, self.text_color, 70, y)
        y = self.draw_text("2 Lines: 100 × Level", self.text_font, self.text_color, 70, y)
        y = self.draw_text("3 Lines: 300 × Level", self.text_font, self.text_color, 70, y)
        y = self.draw_text("4 Lines (Tetris): 1200 × Level", self.text_font, self.text_color, 70, y)
        y = self.draw_text("Combo Bonus: +50% for consecutive clears", self.text_font, self.highlight_color, 70, y)
        y += 20
        
        # Power-ups section
        y = self.draw_text("POWER-UPS (15% chance on line clear):", self.header_font, self.header_color, 50, y)
        
        # Slow Time
        pygame.draw.rect(self.surface, power_up_colors['slow_time'], (70, y + 5, 20, 15))
        y = self.draw_text("Slow Time: Slows down piece falling speed", self.text_font, self.text_color, 100, y)
        
        # Clear Line
        pygame.draw.rect(self.surface, power_up_colors['clear_line'], (70, y + 5, 20, 15))
        y = self.draw_text("Clear Line: Randomly clears a line with blocks", self.text_font, self.text_color, 100, y)
        
        # Bomb
        pygame.draw.rect(self.surface, power_up_colors['bomb'], (70, y + 5, 20, 15))
        y = self.draw_text("Bomb: Clears 3×3 area around current piece", self.text_font, self.text_color, 100, y)
        y += 30
        
        # Instructions
        y = self.draw_text("Press R to close rules and start playing!", self.header_font, self.highlight_color, 50, y)
        
    def toggle(self):
        self.showing = not self.showing
        
    def run(self):
        if self.showing:
            self.draw_rules()
            self.display_surface.blit(self.surface, (0, 0))
