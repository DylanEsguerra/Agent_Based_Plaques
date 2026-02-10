# Abeta Plaque Clearance Agent-Based Model

![Simulation Demo](docs/simulation_demo.gif)

This project is an agent-based model (ABM) designed to simulate the clearance of Amyloid Beta (Abeta) plaques by Microglia and monoclonal Antibodies (mAbs).

## Features
- **Environment**: A grid-based space with two types of plaques:
  - **Diffuse Plaques**: Checkerboard pattern of low-concentration Abeta.
  - **Dense Core Plaques**: Checkerboard pattern with a 5x5 high-concentration core.
- **Agents**:
  - **mAbs (Purple)**: Random walkers that stick to plaques upon contact.
  - **Microglia (Blue/Red)**: 2x2 agents random walkers while in an inactive (blue) state.
- **Microglia Dynamics**:
  - **Activation**: Microglia sense stuck mAbs within a detection radius. If >4 mAbs are detected near a plaque, the microglia activates (turns red) and jumps to the plaque.
  - **Clearance**: Activated microglia clear 1 unit of Abeta concentration from a random plaque cell within their detection radius per step.
  - **Deactivation**: If no plaque remains within the detection radius, the microglia deactivates, turns blue, and releases any stuck mAbs in the area, allowing it to start moving again.

## Requirements
- Python 3.12
- NumPy
- Matplotlib

## Installation
1. Create a virtual environment:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the interactive simulation:
```bash
python main.py
```
