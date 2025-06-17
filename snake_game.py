import pygame
import time
import random
import numpy as np
from enum import Enum
from collections import namedtuple

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


#actions
aciton = [1,0,0]
action = [0,1,0]
action = [0,0,1]

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4

class SnakeAI:
    def __init__(self):
        
        self.width = 640
        self.height = 480
        self.block_size = 20
        
        
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.reset()
        
        
    
    def reset(self):
        self.direction = right
        self.head = [width // 2, height // 2]
        self.snake = [self.head[:], [self.head[0]- block_size, [self.head[1]], self.head[0] - 2 * block_size, self.head[1]]]
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
        
        #move actions
        self.move(action)
        self.snake.insert(0, list(self.head))
        
        #game over lul
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return game_over, self.score, reward
        
        #is snake hungry
        if Point(self.head[0], self.head[1]) == self.food:
            print("Food Eaten!")
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
            reward = 0.1
            
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

    def _update_ui(self):
        self.display.fill(black)
        for pt in self.snake:
            pygame.draw.rect(self.display, green, pygame.Rect(pt[0], pt[1], block_size, block_size))
            pygame.draw.rect(self.display, red, pygame.Rect(self.food[0], self.food[1], block_size, block_size))
        
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(f"Score: {self.score}", True, white)
        self.display.blit(text, [10,10])
        pygame.display.flip()
        
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
    
    
    

        
        