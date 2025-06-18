import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeAI, Direction, Point
from model import LinearQNet, QTrainer
#Constants
MAX_MEMORY = 1000_000
BATCH_SIZE = 10000
LR = 0.001

class Agent:
    
    
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #Amount of Randomness
        self.gamma = 0.9 #Closer to 1 = focused more on long term rewards rather than short term
        self.memory = deque(maxlen=MAX_MEMORY)
        
        self.model = LinearQNet(12,256,3)
        self.trainer = QTrainer(self.model, lr=LR, gamma = 0.9)
        
        
        self.record = 0
        
        
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
        
        dist_x = abs(game.food[0] - head[0])
        dist_y = abs(game.food[1] - head[1])
        max_distance = game.width + game.height
        dist_to_food = (dist_x + dist_y) / max_distance
        
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
            game.food[0] < head[0], #Food is to the left
            game.food[0] > head[0], #Food is to the right
            game.food[1] < head[1], #Food is above
            game.food[1] > head[1], #Food is below
            
            dist_to_food
            
        ]
        
        
        
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        #Stores on game step at a time for memory
        self.memory.append((state, action, reward, next_state, done))
        
    def get_action(self, state):
        #Choose an action, ethier random (exploration mode) or model-base (expidition mode)
        self.epsilon = max(10, 80 - self.n_games // 4) #decreases randomness over number of games played
        final_move = [0,0,0]
        
        
        
        if random.randint(5, 200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            
            if state0.ndim == 1:
                state0 = state0.unsqueeze(0)
            
            predictiction = self.model(state0)
            move = torch.argmax(predictiction).item()
            final_move[move] = 1
        
        return final_move
    
    
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
        #print(f"Eplision{self.epsilon}, Trained!")
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
        print(f"Long Term Memory Trained on {len(mini_sample)} samples.")
        
    def get_relative_directions(self, current_dir):
        if current_dir == Direction.up:
            return [( -1,  0), ( 0, -1), ( 1,  0)]  # left, straight, right
        elif current_dir == Direction.down:
            return [( 1,  0), ( 0,  1), (-1,  0)]
        elif current_dir == Direction.left:
            return [( 0,  1), (-1,  0), ( 0, -1)]
        elif current_dir == Direction.right:
            return [( 0, -1), (1,  0), ( 0,  1)]
        else:
            return [(0,0), (0,0), (0,0)]
        
        
            
        
        
        
        
        