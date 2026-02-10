from environment import PlaqueEnvironment
from visualization import SimulationVisualizer
import os

def main():
    # Initialize environment
    env = PlaqueEnvironment(width=100, height=100)
    
    # Add some Diffuse Plaques
    env.add_diffuse_plaque(center_x=30, center_y=30, radius=10)
    env.add_diffuse_plaque(center_x=70, center_y=20, radius=15)
    
    # Add some Dense Plaques
    env.add_dense_plaque(center_x=50, center_y=60, radius=12)
    env.add_dense_plaque(center_x=20, center_y=80, radius=8)
    
    # Add mAbs (random walkers)
    env.add_mabs(count=150)
    
    # Add Microglia
    env.add_microglia(count=15)
    
    print("Environment initialized with plaques, mAbs, and microglia.")
    
    # Start interactive visualization
    visualizer = SimulationVisualizer(env)
    visualizer.start_animation(interval=50)

if __name__ == "__main__":
    main()
