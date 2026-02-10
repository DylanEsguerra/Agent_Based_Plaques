import numpy as np
import random
from enum import IntEnum

class AbetaConcentration(IntEnum):
    EMPTY = 0
    LOW = 1
    HIGH = 2

class MAb:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.stuck = False

class Microglia:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.activated = False
        self.size = 2

class PlaqueEnvironment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Initialize grid with EMPTY (0)
        self.grid = np.full((height, width), AbetaConcentration.EMPTY, dtype=int)
        # Mask to track the full territory of plaques (even the 'grey' squares)
        self.plaque_mask = np.zeros((height, width), dtype=bool)
        self.mabs = []
        self.microglia = []

    def add_diffuse_plaque(self, center_x: int, center_y: int, radius: int):
        """Adds a diffuse plaque with a checkerboard pattern."""
        for y in range(max(0, center_y - radius), min(self.height, center_y + radius)):
            for x in range(max(0, center_x - radius), min(self.width, center_x + radius)):
                if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                    # Mark this as plaque territory
                    self.plaque_mask[y, x] = True
                    # Checkerboard pattern for concentrations
                    if (x + y) % 2 == 0:
                        self.grid[y, x] = AbetaConcentration.LOW
                    else:
                        self.grid[y, x] = AbetaConcentration.EMPTY

    def add_dense_plaque(self, center_x: int, center_y: int, radius: int):
        """Adds a dense plaque with a checkerboard pattern and a 5x5 high concentration core."""
        self.add_diffuse_plaque(center_x, center_y, radius)
        # 5x5 core (-2 to +2 around center)
        for y in range(max(0, center_y - 2), min(self.height, center_y + 3)):
            for x in range(max(0, center_x - 2), min(self.width, center_x + 3)):
                self.grid[y, x] = AbetaConcentration.HIGH
                self.plaque_mask[y, x] = True

    def add_mabs(self, count: int):
        """Adds a specified number of mAbs at random positions OUTSIDE any plaque territory."""
        for _ in range(count):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                # Ensure they don't start inside ANY plaque territory (even the grey squares)
                if not self.plaque_mask[y, x]:
                    self.mabs.append(MAb(x, y))
                    break

    def add_microglia(self, count: int):
        """Adds a specified number of microglia agents OUTSIDE any plaque territory."""
        for _ in range(count):
            while True:
                # Microglia are 2x2, so we pick the top-left corner
                x = random.randint(0, self.width - 2)
                y = random.randint(0, self.height - 2)
                
                # Check for plaque collision in the 2x2 area
                collision = False
                for ty in range(y, y + 2):
                    for tx in range(x, x + 2):
                        if self.plaque_mask[ty, tx]:
                            collision = True
                            break
                    if collision: break
                
                if not collision:
                    self.microglia.append(Microglia(x, y))
                    break

    def step(self):
        """Advances the simulation by one step."""
        # 1. Move mAbs
        for mab in self.mabs:
            if not mab.stuck:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                new_x = max(0, min(self.width - 1, mab.x + dx))
                new_y = max(0, min(self.height - 1, mab.y + dy))
                mab.x = new_x
                mab.y = new_y
                if self.grid[mab.y, mab.x] > AbetaConcentration.EMPTY:
                    mab.stuck = True
            else:
                # Rule: Re-check if the cell is still a plaque. 
                # If cleared, the mAb might become free or be removed.
                # For now, we'll keep it stuck unless explicitly released.
                pass

        # 2. Update Microglia
        for mg in self.microglia:
            detect_radius = 6
            y_min = max(0, mg.y - detect_radius)
            y_max = min(self.height, mg.y + 2 + detect_radius)
            x_min = max(0, mg.x - detect_radius)
            x_max = min(self.width, mg.x + 2 + detect_radius)

            if not mg.activated:
                # Random walk: ONLY on non-plaque cells
                for _ in range(5):
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                    tx, ty = mg.x + dx, mg.y + dy
                    
                    if 0 <= tx < self.width - 1 and 0 <= ty < self.height - 1:
                        collision = False
                        for y in range(ty, ty + 2):
                            for x in range(tx, tx + 2):
                                if self.plaque_mask[y, x]:
                                    collision = True
                                    break
                            if collision: break
                        
                        if not collision:
                            mg.x, mg.y = tx, ty
                            break

                # Check for activation
                mab_count = 0
                plaque_cells = []
                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        for mab in self.mabs:
                            if mab.stuck and mab.x == x and mab.y == y:
                                mab_count += 1
                        if self.grid[y, x] > 0:
                            plaque_cells.append((x, y))
                
                if mab_count > 4 and plaque_cells:
                    mg.activated = True
                    target_x, target_y = random.choice(plaque_cells)
                    mg.x = max(0, min(self.width - 2, target_x))
                    mg.y = max(0, min(self.height - 2, target_y))
            
            else:
                # Identify all cells with amyloid in the detection radius
                plaque_cells = []
                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        if self.grid[y, x] > 0:
                            plaque_cells.append((x, y))
                
                if plaque_cells:
                    # Randomly pick ONE cell and clear 1 unit
                    cx, cy = random.choice(plaque_cells)
                    current_val = int(self.grid[cy, cx])
                    new_val = current_val - 1
                    self.grid[cy, cx] = AbetaConcentration(new_val)
                    
                    # If cell is now empty, remove from plaque_mask
                    if new_val == 0:
                        self.plaque_mask[cy, cx] = False
                else:
                    # Deactivation logic: if no plaque left in sensing radius
                    mg.activated = False
                    # Clear plaque_mask and release mAbs in the detection radius
                    for y in range(y_min, y_max):
                        for x in range(x_min, x_max):
                            self.plaque_mask[y, x] = False
                            for mab in self.mabs:
                                if mab.stuck and mab.x == x and mab.y == y:
                                    mab.stuck = False

    def get_grid(self):
        return self.grid

    def get_mab_positions(self):
        return [(mab.x, mab.y) for mab in self.mabs]
    
    def get_microglia_data(self):
        """Returns list of (x, y, activated) for microglia."""
        return [(mg.x, mg.y, mg.activated) for mg in self.microglia]
