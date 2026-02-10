from environment import PlaqueEnvironment
from visualization import SimulationVisualizer
import matplotlib.pyplot as plt
import os

def generate_demo():
    # Set seed for reproducibility in demo
    import random
    import numpy as np
    random.seed(42)
    np.random.seed(42)

    # Initialize environment (smaller grid for smaller GIF size)
    env = PlaqueEnvironment(width=80, height=80)
    
    # Add Plaques
    env.add_diffuse_plaque(center_x=20, center_y=25, radius=10)
    env.add_dense_plaque(center_x=50, center_y=50, radius=12)
    
    # Add agents
    env.add_mabs(count=200)
    env.add_microglia(count=20)
    
    os.makedirs("docs", exist_ok=True)
    output_path = "docs/simulation_demo.gif"
    
    
    print("Starting head-less simulation and recording...")
    # Hide the plot window for head-less generation
    plt.ioff()
    
    visualizer = SimulationVisualizer(env)
    # Save a short demo starting from step 0
    visualizer.save_animation(output_path, frames=150, interval=50)
    
    print(f"Demo generated at {output_path}")

if __name__ == "__main__":
    generate_demo()
