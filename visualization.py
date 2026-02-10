import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
import numpy as np
from environment import AbetaConcentration, PlaqueEnvironment

class SimulationVisualizer:
    def __init__(self, env: PlaqueEnvironment):
        self.env = env
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        
        # Colors: 0: Grey, 1: Light Brown, 2: Dark Brown
        colors = ['#808080', '#D2B48C', '#8B4513']
        self.cmap = ListedColormap(colors)
        
        self.img = self.ax.imshow(env.get_grid(), cmap=self.cmap, interpolation='nearest', vmin=0, vmax=2)
        
        # Scatter plot for mAbs (purple squares)
        mab_positions = env.get_mab_positions()
        self.mab_scatter = self.ax.scatter([p[0] for p in mab_positions], 
                                          [p[1] for p in mab_positions], 
                                          c='purple', marker='s', s=40, label='mAb', zorder=3)
            
        # Scatter plots for Microglia (2x2 squares)
        # zorder=4 ensures they are above mAbs and plaques
        self.mg_inactive_scatter = self.ax.scatter([], [], c='skyblue', marker='s', s=160, label='Microglia (Inactive)', zorder=4)
        self.mg_active_scatter = self.ax.scatter([], [], c='red', marker='s', s=160, label='Microglia (Active)', zorder=5)

        self.ax.set_title("Abeta Plaque Clearance Simulation")
        self.ax.axis('off')
        
        # Custom legend
        from matplotlib.lines import Line2D
        self.legend_elements = [
            Line2D([0], [0], marker='s', color='w', label='Empty (Grey)',
                   markerfacecolor='#808080', markersize=15),
            Line2D([0], [0], marker='s', color='w', label='Diffuse Abeta (Light Brown)',
                   markerfacecolor='#D2B48C', markersize=15),
            Line2D([0], [0], marker='s', color='w', label='Dense Core (Dark Brown)',
                   markerfacecolor='#8B4513', markersize=15),
            Line2D([0], [0], marker='s', color='w', label='mAb (Purple)',
                   markerfacecolor='purple', markersize=10),
            Line2D([0], [0], marker='s', color='w', label='Microglia (Blue)',
                   markerfacecolor='skyblue', markersize=15),
            Line2D([0], [0], marker='s', color='w', label='Activated Microglia (Red)',
                   markerfacecolor='red', markersize=15),
        ]
        self.ax.legend(handles=self.legend_elements, loc='upper right')

    def update(self, frame):
        """Update function for animation."""
        self.env.step()
        
        # Update grid image (for clearance)
        self.img.set_data(self.env.get_grid())

        # Update mAb positions
        mab_positions = self.env.get_mab_positions()
        if mab_positions:
            self.mab_scatter.set_offsets(mab_positions)
        
        # Update Microglia positions and colors
        mg_data = self.env.get_microglia_data()
        inactive_pos = []
        active_pos = []
        for x, y, activated in mg_data:
            # Shift by 0.5 to center the 2x2 square on the grid cells
            pos = [x + 0.5, y + 0.5]
            if activated:
                active_pos.append(pos)
            else:
                inactive_pos.append(pos)
        
        if inactive_pos:
            self.mg_inactive_scatter.set_offsets(inactive_pos)
        else:
            self.mg_inactive_scatter.set_offsets(np.empty((0, 2)))

        if active_pos:
            self.mg_active_scatter.set_offsets(active_pos)
        else:
            self.mg_active_scatter.set_offsets(np.empty((0, 2)))
        
        return self.img, self.mab_scatter, self.mg_inactive_scatter, self.mg_active_scatter

    def start_animation(self, interval=50):
        """Starts the interactive animation."""
        ani = FuncAnimation(self.fig, self.update, frames=None, interval=interval, blit=True, cache_frame_data=False)
        plt.show()

def visualize_grid(grid: np.ndarray):
    """Static visualization (kept for compatibility)."""
    colors = ['#808080', '#D2B48C', '#8B4513']
    cmap = ListedColormap(colors)
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=cmap, interpolation='nearest', vmin=0, vmax=2)
    plt.title("Abeta Plaque Clearance Simulation - Environment")
    plt.axis('off')
    plt.show()

def save_grid_image(grid: np.ndarray, filename: str):
    """Saves the grid visualization as an image."""
    colors = ['#808080', '#D2B48C', '#8B4513']
    cmap = ListedColormap(colors)
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=cmap, interpolation='nearest', vmin=0, vmax=2)
    plt.title("Abeta Plaque Clearance Simulation - Environment")
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
