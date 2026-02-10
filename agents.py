import random
from environment import AbetaConcentration

class MAbAgent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_stuck = False

    def step(self, env):
        if self.is_stuck:
            return

        # Simple random walk: move to one of the 8 neighbors or stay
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = max(0, min(env.width - 1, self.x + dx))
        new_y = max(0, min(env.height - 1, self.y + dy))
        
        self.x = new_x
        self.y = new_y
        
        # Check if encountered a plaque
        if env.grid[self.y, self.x] != AbetaConcentration.EMPTY:
            self.is_stuck = True
