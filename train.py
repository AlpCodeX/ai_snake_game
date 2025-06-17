from agent import Agent
from snake_game import SnakeAI

agent = Agent()
game = SnakeAI()

while True:
    #Current State of the Union, I mean game
    state_old = agent.get_state(game)
    
    #Get the next action
    action = agent.get_action(state_old)
    
    #Play the action and get a reward
    done, score, reward = game.play_step(action)
    state_new = agent.get_state(game)
    
    #train short term
    agent.train_short_memory(state_old, action, reward, state_new, done)
    
    #store in memory
    agent.remember(state_old, action, reward, state_new, done)
    
    #if game ends
    if done:
        game.reset()
        agent.n_games += 1
        
        agent.train_long_memory()
    
        if score > agent.record:
            agent.record = score
            agent.model.save()
            
        print(f'Game: {agent.n_games} | Score: {score} | Record: {agent.record}')
    
