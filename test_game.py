import random
from snake_game import SnakeAI
import numpy as np


if __name__ == "__main__":
    game = SnakeAI()
    
    while True:
        #random action
        action = [0,0,0]
        action[random.randint(0,2)] = 1
        
        reward, game_over, score = SnakeAI.play_step(action)
        
        if game_over:
            print(f"Score: {score}")
            break