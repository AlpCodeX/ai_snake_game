import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        torch.save(self.state_dict(), file_name)
        
class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        
    def train_step(self, state, action, reward, next_state, done):
    # Convert to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if isinstance(done, (bool, int)):
            done = torch.tensor([done], dtype=torch.bool)
        else:
            done = torch.tensor(done, dtype=torch.bool)

        # Add batch dimension if needed
        if state.dim() == 1:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)

        # 1. Predict current Q-values
        pred = self.model(state)  # shape: [1, output_size]

        # 2. Clone prediction as target
        target = pred.clone()

        # 3. Calculate new Q value
        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_next = self.model(next_state[i].unsqueeze(0))
                Q_new = reward[i] + self.gamma * torch.max(Q_next)

            action_index = torch.argmax(action[i]).item()
            target[i][action_index] = Q_new

        # 5. Optimize
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
