#!/usr/bin/env python3
"""
Pacman-Nibbles Game
A combination of Pacman and Snake (Nibbles) game mechanics.
"""

import pygame
import sys
import random
import os
import math
from collections import deque
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # Lower is faster

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create a directory for assets if it doesn't exist
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Function to create simple image assets
def create_assets():
    # Create snake head image
    snake_head_img = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(snake_head_img, GREEN, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
    # Add eyes
    pygame.draw.circle(snake_head_img, WHITE, (GRID_SIZE*3//4, GRID_SIZE//3), GRID_SIZE//6)
    pygame.draw.circle(snake_head_img, WHITE, (GRID_SIZE*3//4, GRID_SIZE*2//3), GRID_SIZE//6)
    pygame.draw.circle(snake_head_img, BLACK, (GRID_SIZE*3//4, GRID_SIZE//3), GRID_SIZE//10)
    pygame.draw.circle(snake_head_img, BLACK, (GRID_SIZE*3//4, GRID_SIZE*2//3), GRID_SIZE//10)
    
    # Create snake body segment
    snake_body_img = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(snake_body_img, GREEN, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 1)
    
    # Create ghost images
    ghost_imgs = {}
    ghost_colors = {
        'red': RED,
        'pink': PINK,
        'cyan': CYAN,
        'orange': ORANGE
    }
    
    for color_name, color in ghost_colors.items():
        ghost_img = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Ghost body (rounded top, straight bottom)
        pygame.draw.rect(ghost_img, color, (0, GRID_SIZE//2, GRID_SIZE, GRID_SIZE//2))
        pygame.draw.circle(ghost_img, color, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
        
        # Create wavy bottom
        for i in range(3):
            pygame.draw.circle(ghost_img, color, 
                              (i * GRID_SIZE//3 + GRID_SIZE//6, GRID_SIZE), 
                              GRID_SIZE//6)
        
        # Eyes
        pygame.draw.circle(ghost_img, WHITE, (GRID_SIZE//3, GRID_SIZE//2), GRID_SIZE//5)
        pygame.draw.circle(ghost_img, WHITE, (GRID_SIZE*2//3, GRID_SIZE//2), GRID_SIZE//5)
        pygame.draw.circle(ghost_img, BLACK, (GRID_SIZE//3, GRID_SIZE//2), GRID_SIZE//8)
        pygame.draw.circle(ghost_img, BLACK, (GRID_SIZE*2//3, GRID_SIZE//2), GRID_SIZE//8)
        
        ghost_imgs[color_name] = ghost_img
    
    # Create scared ghost (blue)
    scared_ghost_img = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(scared_ghost_img, BLUE, (0, GRID_SIZE//2, GRID_SIZE, GRID_SIZE//2))
    pygame.draw.circle(scared_ghost_img, BLUE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
    
    # Create wavy bottom
    for i in range(3):
        pygame.draw.circle(scared_ghost_img, BLUE, 
                          (i * GRID_SIZE//3 + GRID_SIZE//6, GRID_SIZE), 
                          GRID_SIZE//6)
    
    # Scared eyes
    pygame.draw.line(scared_ghost_img, WHITE, (GRID_SIZE//4, GRID_SIZE//3), 
                    (GRID_SIZE//2 - 2, GRID_SIZE//2), 2)
    pygame.draw.line(scared_ghost_img, WHITE, (GRID_SIZE//4, GRID_SIZE//2), 
                    (GRID_SIZE//2 - 2, GRID_SIZE//3), 2)
    pygame.draw.line(scared_ghost_img, WHITE, (GRID_SIZE*3//4, GRID_SIZE//3), 
                    (GRID_SIZE//2 + 2, GRID_SIZE//2), 2)
    pygame.draw.line(scared_ghost_img, WHITE, (GRID_SIZE*3//4, GRID_SIZE//2), 
                    (GRID_SIZE//2 + 2, GRID_SIZE//3), 2)
    
    # Create wall tile with brick pattern
    wall_img = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    wall_color = (0, 0, 180)  # Darker blue for walls
    highlight = (100, 100, 255)  # Lighter blue for highlights
    shadow = (0, 0, 100)  # Darker blue for shadows
    
    # Fill background
    pygame.draw.rect(wall_img, wall_color, (0, 0, GRID_SIZE, GRID_SIZE))
    
    # Create brick pattern
    brick_height = GRID_SIZE // 4
    mortar_thickness = 2
    
    # First row - full bricks
    pygame.draw.rect(wall_img, shadow, (0, 0, GRID_SIZE, mortar_thickness))
    pygame.draw.rect(wall_img, shadow, (0, brick_height - mortar_thickness, GRID_SIZE, mortar_thickness))
    
    # Second row - half brick offset
    pygame.draw.rect(wall_img, shadow, (0, brick_height, GRID_SIZE, mortar_thickness))
    pygame.draw.rect(wall_img, shadow, (0, 2 * brick_height - mortar_thickness, GRID_SIZE, mortar_thickness))
    pygame.draw.rect(wall_img, shadow, (GRID_SIZE // 2 - mortar_thickness // 2, brick_height, mortar_thickness, brick_height))
    
    # Third row - full bricks
    pygame.draw.rect(wall_img, shadow, (0, 2 * brick_height, GRID_SIZE, mortar_thickness))
    pygame.draw.rect(wall_img, shadow, (0, 3 * brick_height - mortar_thickness, GRID_SIZE, mortar_thickness))
    
    # Fourth row - half brick offset
    pygame.draw.rect(wall_img, shadow, (0, 3 * brick_height, GRID_SIZE, mortar_thickness))
    pygame.draw.rect(wall_img, shadow, (0, 4 * brick_height - mortar_thickness, GRID_SIZE, mortar_thickness))
    pygame.draw.rect(wall_img, shadow, (GRID_SIZE // 2 - mortar_thickness // 2, 3 * brick_height, mortar_thickness, brick_height))
    
    # Vertical mortar lines for full brick rows
    pygame.draw.rect(wall_img, shadow, (GRID_SIZE // 2 - mortar_thickness // 2, 0, mortar_thickness, brick_height))
    pygame.draw.rect(wall_img, shadow, (GRID_SIZE // 2 - mortar_thickness // 2, 2 * brick_height, mortar_thickness, brick_height))
    
    # Add some highlights to give 3D effect
    for i in range(4):
        y = i * brick_height + 2
        pygame.draw.line(wall_img, highlight, (2, y), (GRID_SIZE - 2, y), 1)
    
    return {
        'snake_head': snake_head_img,
        'snake_body': snake_body_img,
        'ghost_red': ghost_imgs['red'],
        'ghost_pink': ghost_imgs['pink'],
        'ghost_cyan': ghost_imgs['cyan'],
        'ghost_orange': ghost_imgs['orange'],
        'ghost_scared': scared_ghost_img,
        'wall': wall_img
    }

class PacNibbles:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman-Nibbles")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.snake = deque()
        self.walls = []
        self.dots = []
        self.power_pellets = []
        self.ghosts = []
        
        # Load game assets
        self.assets = create_assets()
        
        # Create rotated versions of the snake head
        self.rotated_heads = {
            UP: pygame.transform.rotate(self.assets['snake_head'], 90),
            DOWN: pygame.transform.rotate(self.assets['snake_head'], -90),
            LEFT: pygame.transform.rotate(self.assets['snake_head'], 180),
            RIGHT: self.assets['snake_head']
        }
        
        # Ghost colors
        self.ghost_colors = ['ghost_red', 'ghost_pink', 'ghost_cyan', 'ghost_orange']
        
        self.reset_game()

    def reset_game(self):
        # Snake properties
        self.snake = deque([(GRID_WIDTH // 2, GRID_HEIGHT // 2)])
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.game_over = False
        
        # Generate maze walls
        self.walls = self.generate_maze()
        
        # Generate dots
        self.dots = []
        self.generate_dots(30)  # Start with 30 dots
        
        # Generate power pellets
        self.power_pellets = []
        self.generate_power_pellets(4)  # 4 power pellets
        
        # Ghosts
        self.ghosts = []
        # Delay ghost generation to give player a head start
        self.ghost_spawn_time = pygame.time.get_ticks() + 3000  # 3 seconds delay
        self.ghosts_to_spawn = 3
        
        # Power-up state
        self.powered_up = False
        self.power_time = 0
        
        # Display a "Get Ready" message
        self.show_get_ready = True
        self.get_ready_time = pygame.time.get_ticks()
        
    def generate_maze(self):
        walls = []
        
        # Border walls
        for x in range(GRID_WIDTH):
            walls.append((x, 0))
            walls.append((x, GRID_HEIGHT - 1))
        
        for y in range(GRID_HEIGHT):
            walls.append((0, y))
            walls.append((GRID_WIDTH - 1, y))
        
        # Create a safe zone around the snake's starting position
        safe_zone_radius = 5
        snake_head_x, snake_head_y = self.snake[0]
        safe_zone = []
        
        for x in range(snake_head_x - safe_zone_radius, snake_head_x + safe_zone_radius + 1):
            for y in range(snake_head_y - safe_zone_radius, snake_head_y + safe_zone_radius + 1):
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    safe_zone.append((x, y))
        
        # Generate random wall patterns
        wall_patterns = []
        
        # Add some horizontal barriers
        num_h_barriers = random.randint(3, 5)
        for _ in range(num_h_barriers):
            start_x = random.randint(5, GRID_WIDTH - 15)
            start_y = random.randint(5, GRID_HEIGHT - 5)
            length = random.randint(5, 10)
            
            pattern = []
            for i in range(length):
                pattern.append((start_x + i, start_y))
            wall_patterns.append(pattern)
        
        # Add some vertical barriers
        num_v_barriers = random.randint(3, 5)
        for _ in range(num_v_barriers):
            start_x = random.randint(5, GRID_WIDTH - 5)
            start_y = random.randint(5, GRID_HEIGHT - 15)
            length = random.randint(5, 10)
            
            pattern = []
            for i in range(length):
                pattern.append((start_x, start_y + i))
            wall_patterns.append(pattern)
        
        # Add some small wall sections
        small_patterns = [
            # Small square
            [(x, y), (x+1, y), (x, y+1), (x+1, y+1)] 
            for x in range(5, GRID_WIDTH-10, 10) 
            for y in range(5, GRID_HEIGHT-10, 10)
        ]
        
        # L shapes
        for _ in range(3):
            x = random.randint(5, GRID_WIDTH - 7)
            y = random.randint(5, GRID_HEIGHT - 7)
            small_patterns.append([(x, y), (x+1, y), (x, y+1)])
        
        # T shapes
        for _ in range(3):
            x = random.randint(5, GRID_WIDTH - 7)
            y = random.randint(5, GRID_HEIGHT - 7)
            small_patterns.append([(x, y), (x-1, y), (x+1, y), (x, y+1)])
        
        # Randomly select some patterns to use
        selected_patterns = random.sample(small_patterns, min(len(small_patterns), 5))
        wall_patterns.extend(selected_patterns)
        
        # Add walls from patterns, avoiding the safe zone
        for pattern in wall_patterns:
            for wall in pattern:
                if wall not in walls and wall not in safe_zone:
                    walls.append(wall)
        
        return walls
    
    def generate_dots(self, count):
        self.dots = []
        for _ in range(count):
            self.place_dot()
    
    def place_dot(self):
        while True:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            if (x, y) not in self.snake and (x, y) not in self.walls and (x, y) not in self.dots and (x, y) not in self.power_pellets:
                self.dots.append((x, y))
                break
    
    def generate_power_pellets(self, count):
        self.power_pellets = []
        for _ in range(count):
            while True:
                x = random.randint(1, GRID_WIDTH - 2)
                y = random.randint(1, GRID_HEIGHT - 2)
                if (x, y) not in self.snake and (x, y) not in self.walls and (x, y) not in self.dots and (x, y) not in self.power_pellets:
                    self.power_pellets.append((x, y))
                    break
    
    def generate_ghosts(self, count):
        self.ghosts = []
        for _ in range(count):
            while True:
                x = random.randint(1, GRID_WIDTH - 2)
                y = random.randint(1, GRID_HEIGHT - 2)
                # Make sure ghosts are not too close to the snake
                if (x, y) not in self.snake and (x, y) not in self.walls and \
                   abs(x - self.snake[0][0]) > 5 and abs(y - self.snake[0][1]) > 5:
                    self.ghosts.append({
                        'pos': (x, y),
                        'direction': random.choice([UP, DOWN, LEFT, RIGHT]),
                        'color': random.choice(self.ghost_colors)
                    })
                    break
    
    def move_snake(self):
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        # Check for collisions with walls
        if new_head in self.walls:
            self.game_over = True
            return
        
        # Check for collision with self
        if new_head in list(self.snake)[1:]:
            self.game_over = True
            return
        
        # Move the snake
        self.snake.appendleft(new_head)
        
        # Check for dot collision
        if new_head in self.dots:
            self.dots.remove(new_head)
            self.score += 10
            self.place_dot()
            # Don't remove the tail to make the snake grow
        else:
            # Check for power pellet collision
            if new_head in self.power_pellets:
                self.power_pellets.remove(new_head)
                self.powered_up = True
                self.power_time = pygame.time.get_ticks()
                self.score += 50
            else:
                # If no dot or power pellet was eaten, remove the tail
                self.snake.pop()
        
        # Check for ghost collision
        for ghost in self.ghosts[:]:  # Create a copy to safely modify during iteration
            if new_head == ghost['pos']:
                if self.powered_up:
                    # Eat the ghost
                    self.ghosts.remove(ghost)
                    self.score += 200
                    # Spawn a new ghost
                    self.generate_ghosts(1)
                else:
                    self.game_over = True
                    return
    
    def move_ghosts(self):
        for ghost in self.ghosts:
            # Decide whether to change direction
            if random.random() < 0.2:
                # 20% chance to change direction randomly
                ghost['direction'] = random.choice([UP, DOWN, LEFT, RIGHT])
            elif random.random() < 0.6:
                # 60% chance to move towards or away from the snake based on power-up state
                head_x, head_y = self.snake[0]
                ghost_x, ghost_y = ghost['pos']
                
                # Determine direction to move
                if self.powered_up:
                    # Run away from snake
                    if ghost_x < head_x:
                        ghost['direction'] = LEFT
                    elif ghost_x > head_x:
                        ghost['direction'] = RIGHT
                    elif ghost_y < head_y:
                        ghost['direction'] = UP
                    else:
                        ghost['direction'] = DOWN
                else:
                    # Chase the snake
                    if ghost_x < head_x:
                        ghost['direction'] = RIGHT
                    elif ghost_x > head_x:
                        ghost['direction'] = LEFT
                    elif ghost_y < head_y:
                        ghost['direction'] = DOWN
                    else:
                        ghost['direction'] = UP
            
            # Calculate new position
            dx, dy = ghost['direction']
            ghost_x, ghost_y = ghost['pos']
            new_pos = ((ghost_x + dx) % GRID_WIDTH, (ghost_y + dy) % GRID_HEIGHT)
            
            # Check if the new position is valid
            if new_pos not in self.walls:
                ghost['pos'] = new_pos
            else:
                # If hitting a wall, choose a random valid direction
                valid_directions = []
                for direction in [UP, DOWN, LEFT, RIGHT]:
                    dx, dy = direction
                    check_pos = ((ghost_x + dx) % GRID_WIDTH, (ghost_y + dy) % GRID_HEIGHT)
                    if check_pos not in self.walls:
                        valid_directions.append(direction)
                
                if valid_directions:
                    ghost['direction'] = random.choice(valid_directions)
    
    def check_power_up(self):
        if self.powered_up and pygame.time.get_ticks() - self.power_time > 5000:  # 5 seconds of power
            self.powered_up = False
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw walls with brick pattern
        for wall in self.walls:
            self.screen.blit(self.assets['wall'], 
                           (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE))
        
        # Draw dots
        for dot in self.dots:
            pygame.draw.circle(self.screen, WHITE, 
                              (dot[0] * GRID_SIZE + GRID_SIZE // 2, 
                               dot[1] * GRID_SIZE + GRID_SIZE // 2), 
                              GRID_SIZE // 5)
        
        # Draw power pellets
        for pellet in self.power_pellets:
            pygame.draw.circle(self.screen, WHITE, 
                              (pellet[0] * GRID_SIZE + GRID_SIZE // 2, 
                               pellet[1] * GRID_SIZE + GRID_SIZE // 2), 
                              GRID_SIZE // 2.5)
            # Add pulsating effect
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2 + 2
            pygame.draw.circle(self.screen, YELLOW, 
                              (pellet[0] * GRID_SIZE + GRID_SIZE // 2, 
                               pellet[1] * GRID_SIZE + GRID_SIZE // 2), 
                              pulse)
        
        # Draw snake
        # First draw the body segments
        for i, segment in enumerate(list(self.snake)[1:]):
            self.screen.blit(self.assets['snake_body'], 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        
        # Then draw the head with proper rotation
        if self.snake:
            head_pos = self.snake[0]
            self.screen.blit(self.rotated_heads[self.direction], 
                           (head_pos[0] * GRID_SIZE, head_pos[1] * GRID_SIZE))
        
        # Draw ghosts
        for ghost in self.ghosts:
            if self.powered_up:
                ghost_img = self.assets['ghost_scared']
            else:
                ghost_img = self.assets[ghost['color']]
            
            self.screen.blit(ghost_img, 
                           (ghost['pos'][0] * GRID_SIZE, ghost['pos'][1] * GRID_SIZE))
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw "Get Ready" message
        if self.show_get_ready:
            if pygame.time.get_ticks() - self.get_ready_time < 2000:  # Show for 2 seconds
                ready_text = self.font.render('Get Ready!', True, YELLOW)
                text_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(ready_text, text_rect)
            else:
                self.show_get_ready = False
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to restart', True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.next_direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.next_direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.next_direction = RIGHT
    
    def run(self):
        while True:
            self.handle_events()
            
            if not self.game_over:
                # Check if it's time to spawn ghosts
                current_time = pygame.time.get_ticks()
                if self.ghosts_to_spawn > 0 and current_time >= self.ghost_spawn_time:
                    self.generate_ghosts(1)
                    self.ghosts_to_spawn -= 1
                    self.ghost_spawn_time = current_time + 1000  # 1 second between spawns
                
                self.move_snake()
                self.move_ghosts()
                self.check_power_up()
            
            self.draw()
            self.clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    game = PacNibbles()
    game.run()
