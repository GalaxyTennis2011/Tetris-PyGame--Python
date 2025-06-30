
from settings import *
from random import choice, randint
from sys import exit
from os.path import join
import math

from timer import Timer

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vel_x = randint(-3, 3)
        self.vel_y = randint(-5, -1)
        self.color = color
        self.life = 30
        self.max_life = 30
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2  # gravity
        self.life -= 1
        
    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        size = max(1, int(4 * (self.life / self.max_life)))
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.collected = False
        self.glow_timer = 0
        
    def update(self):
        self.glow_timer += 0.2
        
    def draw(self, surface):
        glow_intensity = int(50 + 30 * math.sin(self.glow_timer))
        color = power_up_colors[self.power_type]
        
        # Draw glowing effect
        for i in range(3):
            alpha = glow_intensity - i * 15
            if alpha > 0:
                s = pygame.Surface((cell_size + i * 4, cell_size + i * 4))
                s.set_alpha(alpha)
                s.fill(color)
                surface.blit(s, (self.x * cell_size - i * 2, self.y * cell_size - i * 2))

class Game:
    def __init__(self, get_next_shape, update_score):
        # general 
        self.surface = pygame.Surface((game_width, game_height))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (padding, padding))
        self.sprites = pygame.sprite.Group()

        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # lines 
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # tetromino
        self.field_data = [[0 for x in range(columns)] for y in range(rows)]
        self.tetromino = Tetromino(
            choice(list(tetrominos.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

        # timer 
        self.down_speed = update_start_speed
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(move_wait_time),
            'rotate': Timer(rotate_wait_time)
        }
        self.timers['vertical move'].activate()

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.combo_count = 0
        self.last_clear_time = 0

        # power-ups
        self.power_ups = []
        self.active_power_up = None
        self.power_up_timer = 0
        self.slow_time_active = False
        self.clear_line_active = False
        
        # particles
        self.particles = []
        
        # ghost piece
        self.ghost_blocks = []

        # sound 
        self.landing_sound = pygame.mixer.Sound(join('Sound', 'landing.wav'))
        self.landing_sound.set_volume(0.1)

    def create_ghost_piece(self):
        self.ghost_blocks = []
        if self.tetromino:
            # Create ghost blocks at current position
            for block in self.tetromino.blocks:
                ghost_pos = pygame.Vector2(block.pos.x, block.pos.y)
                
                # Drop ghost piece down until collision
                while not self.would_collide_vertical(ghost_pos, 1):
                    ghost_pos.y += 1
                    
                self.ghost_blocks.append(ghost_pos)
    
    def would_collide_vertical(self, pos, amount):
        new_y = int(pos.y + amount)
        if new_y >= rows:
            return True
        if new_y >= 0 and self.field_data[new_y][int(pos.x)]:
            return True
        return False

    def spawn_power_up(self, x, y):
        if randint(1, 100) <= 15:  # 15% chance
            power_type = choice(list(power_up_types.keys()))
            self.power_ups.append(PowerUp(x, y, power_type))

    def collect_power_up(self, x, y):
        for power_up in self.power_ups:
            if power_up.x == x and power_up.y == y and not power_up.collected:
                power_up.collected = True
                self.activate_power_up(power_up.power_type)
                self.power_ups.remove(power_up)
                break

    def activate_power_up(self, power_type):
        self.active_power_up = power_type
        self.power_up_timer = power_up_duration
        
        if power_type == 'slow_time':
            self.slow_time_active = True
            self.timers['vertical move'].duration = self.down_speed * 2
        elif power_type == 'clear_line':
            self.clear_random_line()
        elif power_type == 'bomb':
            self.explode_area()

    def clear_random_line(self):
        # Find lines with blocks
        lines_with_blocks = []
        for i, row in enumerate(self.field_data):
            if any(row):
                lines_with_blocks.append(i)
        
        if lines_with_blocks:
            line_to_clear = choice(lines_with_blocks)
            # Clear the line
            for block in self.field_data[line_to_clear]:
                if block:
                    # Add particles
                    for _ in range(10):
                        self.particles.append(Particle(
                            block.pos.x * cell_size + cell_size // 2,
                            block.pos.y * cell_size + cell_size // 2,
                            block.image.get_at((cell_size // 2, cell_size // 2))[:3]
                        ))
                    block.kill()
            
            # Move blocks down
            for row in self.field_data:
                for block in row:
                    if block and block.pos.y < line_to_clear:
                        block.pos.y += 1
            
            # Rebuild field data
            self.field_data = [[0 for x in range(columns)] for y in range(rows)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

    def explode_area(self):
        # Clear 3x3 area around current piece
        if self.tetromino and self.tetromino.blocks:
            center = self.tetromino.blocks[0].pos
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    x, y = int(center.x + dx), int(center.y + dy)
                    if 0 <= x < columns and 0 <= y < rows and self.field_data[y][x]:
                        block = self.field_data[y][x]
                        # Add particles
                        for _ in range(8):
                            self.particles.append(Particle(
                                x * cell_size + cell_size // 2,
                                y * cell_size + cell_size // 2,
                                (255, 100, 0)  # Orange explosion
                            ))
                        block.kill()
                        self.field_data[y][x] = 0

    def update_power_ups(self):
        if self.active_power_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                if self.active_power_up == 'slow_time':
                    self.slow_time_active = False
                    self.timers['vertical move'].duration = self.down_speed
                self.active_power_up = None
        
        for power_up in self.power_ups:
            power_up.update()

    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        
        # Combo system
        current_time = pygame.time.get_ticks()
        if current_time - self.last_clear_time < 3000:  # 3 seconds
            self.combo_count += 1
        else:
            self.combo_count = 1
        
        self.last_clear_time = current_time
        
        # Calculate score with combo bonus
        base_score = score_data[num_lines] * self.current_level
        combo_bonus = base_score * (self.combo_count - 1) * 0.5
        self.current_score += int(base_score + combo_bonus)

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            if not self.slow_time_active:
                self.timers['vertical move'].duration = self.down_speed

        self.update_score(self.current_lines, self.current_score, self.current_level)

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                exit()

    def create_new_tetromino(self):
        self.landing_sound.play()
        self.check_game_over()
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, columns):
            x = col * cell_size
            pygame.draw.line(self.line_surface, line_color, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, rows):
            y = row * cell_size
            pygame.draw.line(self.line_surface, line_color, (0,y), (self.surface.get_width(),y))

        self.surface.blit(self.line_surface, (0,0))

    def draw_ghost_piece(self):
        for ghost_pos in self.ghost_blocks:
            ghost_rect = pygame.Rect(ghost_pos.x * cell_size, ghost_pos.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(self.surface, (100, 100, 100), ghost_rect)
            pygame.draw.rect(self.surface, line_color, ghost_rect, 2)

    def draw_power_ups(self):
        for power_up in self.power_ups:
            power_up.draw(self.surface)

    def draw_particles(self):
        for particle in self.particles:
            particle.draw(self.surface)

    def draw_combo_text(self):
        if self.combo_count > 1:
            font = pygame.font.Font(None, 36)
            combo_text = font.render(f"COMBO x{self.combo_count}!", True, (255, 255, 0))
            self.surface.blit(combo_text, (10, 10))

    def input(self):
        keys = pygame.key.get_pressed()

        # checking horizontal movement
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)	
                self.timers['horizontal move'].activate()

        # check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            current_speed = self.down_speed * 2 if self.slow_time_active else self.down_speed
            self.timers['vertical move'].duration = current_speed * 0.3

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            current_speed = self.down_speed * 2 if self.slow_time_active else self.down_speed
            self.timers['vertical move'].duration = current_speed

    def check_finished_rows(self):
        # get the full row indexes 
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                # Create particles for cleared line
                for x in range(columns):
                    block = self.field_data[delete_row][x]
                    if block:
                        # Collect power-ups
                        self.collect_power_up(x, delete_row)
                        
                        # Add particles
                        for _ in range(5):
                            self.particles.append(Particle(
                                x * cell_size + cell_size // 2,
                                delete_row * cell_size + cell_size // 2,
                                block.image.get_at((cell_size // 2, cell_size // 2))[:3]
                            ))
                        
                        # Chance to spawn power-up
                        self.spawn_power_up(x, delete_row - 1)
                        
                        block.kill()

                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            # rebuild the field data 
            self.field_data = [[0 for x in range(columns)] for y in range(rows)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            # update score
            self.calculate_score(len(delete_rows))

    def run(self):
        # update
        self.input()
        self.timer_update()
        self.update_power_ups()
        self.update_particles()
        self.sprites.update()
        self.create_ghost_piece()

        # drawing 
        self.surface.fill(gray)
        
        # Draw ghost piece first (behind everything)
        self.draw_ghost_piece()
        
        # Draw main game elements
        self.sprites.draw(self.surface)
        self.draw_power_ups()
        self.draw_particles()
        self.draw_combo_text()
        
        self.draw_grid()
        self.display_surface.blit(self.surface, (padding,padding))
        pygame.draw.rect(self.display_surface, line_color, self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        # setup 
        self.shape = shape
        self.block_positions = tetrominos[shape]['shape']
        self.color = tetrominos[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    # movement
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    # rotate
    def rotate(self):
        if self.shape != 'O':
            # 1. pivot point 
            pivot_pos = self.blocks[0].pos

            # 2. new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # 3. collision check with wall kicks
            for kick_x, kick_y in [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]:
                valid = True
                test_positions = []
                
                for pos in new_block_positions:
                    test_pos = pygame.Vector2(pos.x + kick_x, pos.y + kick_y)
                    test_positions.append(test_pos)
                    
                    # horizontal bounds check
                    if test_pos.x < 0 or test_pos.x >= columns:
                        valid = False
                        break
                    
                    # vertical bounds check
                    if test_pos.y >= rows:
                        valid = False
                        break
                    
                    # field collision check
                    if test_pos.y >= 0 and self.field_data[int(test_pos.y)][int(test_pos.x)]:
                        valid = False
                        break
                
                if valid:
                    # Apply the rotation with kick
                    for i, block in enumerate(self.blocks):
                        block.pos = test_positions[i]
                    break

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        # general
        super().__init__(group)
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(color)
        
        # Add border for better visual
        pygame.draw.rect(self.image, line_color, self.image.get_rect(), 2)

        # position
        self.pos = pygame.Vector2(pos) + block_offset
        self.rect = self.image.get_rect(topleft = self.pos * cell_size)

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < columns:
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= rows:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * cell_size
