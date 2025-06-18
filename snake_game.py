import pygame
import time
import random
import numpy as np
from enum import Enum
from collections import namedtuple, deque
import torch

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 25)

#Dimesions
width = 640
height = 480
block_size = 20

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

#Directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)




Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4

class SnakeAI:
    def __init__(self, agent=None):
        
        self.width = 640
        self.height = 480
        self.block_size = 20
        
        
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.reset()
        self.agent = agent
        
        self.prev_positions = deque(maxlen=20)
        
        
    
    def reset(self):
        self.direction = right
        self.head = [width // 2, height // 2]
        self.snake = [
            self.head[:], 
            [self.head[0]- block_size, self.head[1]],
            [self.head[0] - 2 * block_size, self.head[1]]]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(0, (width - block_size) // block_size) * block_size
        y = random.randint(0, (height - block_size) // block_size) * block_size
        self.food = Point(x,y)
        if self.food  in self.snake:
            self._place_food()
                
    
    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
                quit()
        
        reward = 0
        #move actions
        distance_before = self._distance_to_food(self.head)
        self.move(action)
        self.snake.insert(0, list(self.head))
        distance_after = self._distance_to_food(self.head)
        self.prev_positions.append(tuple(self.head))
        
        detla_distance = distance_before - distance_after
        reward += detla_distance * 2
        
        
        loop_count = self.prev_positions.count(tuple(self.head))
        
        if loop_count > 2:
            reward -= 50
        
        #game over lul
        
        game_over = False
        if self._is_collision() or self.frame_iteration > 80 * len(self.snake):
            game_over = True
            reward -= 20
            return game_over, self.score, reward
        
        #is snake hungry
        if Point(self.head[0], self.head[1]) == self.food:
            print("Food Eaten!")
            self.score += 1
            reward += 20
            self._place_food()
        else:
            self.snake.pop()
            reward -= 0.1
            
       
        
            
        self._update_ui()
        self.clock.tick(60)
        
        return game_over, self.score, reward
    
    def _is_collision(self, pt=None):
        if pt == None:
            pt = self.head
        
        #Check if head bonked on wall
        if pt[0] < 0 or pt[0] >= width or pt[1] < 0 or pt[1] >= height:
            return True
        
        #Check if tried to eat self
        if pt in self.snake[1:]:
            return True
        
        return False
    
    def _distance_to_food(self, pos):
        return abs(pos[0] - self.food.x) + abs(pos[1] - self.food.y)

    def _update_ui(self):
        self.display.fill(black)
        if self.agent:
            self.draw_heatmap(self.agent)
        for pt in self.snake:
            pygame.draw.rect(self.display, green, pygame.Rect(pt[0], pt[1], block_size, block_size))
        
        pygame.draw.rect(self.display, red, pygame.Rect(self.food[0], self.food[1], block_size, block_size))
        
       
        
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(f"Score: {self.score}", True, white)
        self.display.blit(text, [10,10])
        pygame.display.flip()
        
        if hasattr(self, "agent_state"):
            state_text = font.render(f"State: {self.agent_state}", True, (200, 200, 200))
            self.display.blit(state_text, [10,70])
        
    def move(self, action):
    # [straight, right, left]
        clockwise = [right, down, left, up]
        idx = clockwise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clockwise[idx]  # straight
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clockwise[(idx + 1) % 4]  # right turn
        else:  # [0, 0, 1]
            new_dir = clockwise[(idx - 1) % 4]  # left turn

        self.direction = new_dir

        x, y = self.head
        dx, dy = self.direction
        self.head = [x + dx * block_size, y + dy * block_size]
        
    def draw_heatmap(self, agent):
        head = self.snake[0]

        # Get current state
        state = agent.get_state(self)
        state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0)

        # Predict Q-values
        q_values = agent.model(state_tensor).detach().numpy()[0]  # [Q_left, Q_straight, Q_right]

        # Normalize for coloring
        q_min, q_max = min(q_values), max(q_values)
        q_range = q_max - q_min if q_max != q_min else 1e-5

        colors = []
        for q in q_values:
            # Interpolate red intensity: high Q → brighter red
            intensity = int(255 * (q - q_min) / q_range)
            colors.append((intensity, 0, 0))  # (R, G, B)

        # Directions relative to current heading
        directions = agent.get_relative_directions(self.direction)

        for dir_vector, color in zip(directions, colors):
            dx, dy = dir_vector
            x = head[0] + dx * self.block_size
            y = head[1] + dy * self.block_size

            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(self.display, color, rect, border_radius=4)



            
        
        
        
        
                
                
        
            
        
        
        
        


    
        
def show_game_over(score):
    screen.fill(black)
    game_over_text = font.render("GAME OVER", True, red)
    score_text = font.render(f"Final Score: {score}", True, white)
    prompt_text = font.render("Press Q to Quit or R to Restart", True, white)
    
    screen.blit(game_over_text, [width //2 - 80, height //2 - 60])
    screen.blit(score_text, [width //2 - 100, height // 2 - 20])
    screen.blit(prompt_text, [width // 2 - 180, height // 2 + 20])
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    main()
                    
    
def draw_score(score):
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, [10,10])
    
    
    

        
        