import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeAI, Direction, Point
from model import LinearQNet, QTrainer
#Constants
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #Amount of Randomness
        self.gamma = 0.9 #Closer to 1 = focused more on long term rewards rather than short term
        self.memory = deque(maxlen=MAX_MEMORY)
        
        self.model = LinearQNet(11,256,3)
        self.trainer = QTrainer(self.model, lr=LR, gamma = 0.9)
        
    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head[0] - game.block_size, head[1])
        point_r = Point(head[0] + game.block_size, head[1])
        point_u = Point(head[0], head[1] + game.block_size)
        point_d = Point(head[0], head[1] - game.block_size)
        
        dir_l = game.direction == Direction.left
        dir_r = game.direction == Direction.right
        dir_u = game.direction == Direction.up
        dir_d = game.direction == Direction.down
        
        state = [
            #Check to see if there is danger straight ahead
            (dir_r and game._is_collision(point_r)) or
            (dir_l and game._is_collision(point_l)) or
            (dir_u) and game._is_collision(point_u) or
            (dir_d) and game._is_collision(point_d), 
            
            # Danger right
            (dir_u and game._is_collision(point_r)) or
            (dir_d and game._is_collision(point_l)) or
            (dir_l and game._is_collision(point_u)) or
            (dir_r and game._is_collision(point_d)),

            # Danger left
            (dir_d and game._is_collision(point_r)) or
            (dir_u and game._is_collision(point_l)) or
            (dir_r and game._is_collision(point_u)) or
            (dir_l and game._is_collision(point_d)),
            
            #Directions to Move
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            #Food Checks
            game.food[0] < game.head[0], #Food is to the left
            game.food[0] > game.head[0], #Food is to the right
            game.food[0] > game.head[1], #Food is above
            game.food[0] < game.head[1] #Food is below
            
        ]
        
        return np.array(state, dype=int)
    
    def remember(self, state, action, reward, next_step, done):
        #Stores on game step at a time for memory
        self.memory.append((state, action, reward, next_step, done))
        
    def get_action(self, state):
        #Choose an action, ethier random (exploration mode) or model-base (expidition mode)
        self.epsilon = 80 - self.n_games #decreases randomness over number of games played
        final_move = [0,0,0]
        
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            predictiction = self.model(state0)
            move = torch.argmax(predictiction).item()
            final_move[move] = 1
        
        return final_move
            
        
        
        
        
        