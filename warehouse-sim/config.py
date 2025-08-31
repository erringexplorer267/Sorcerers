# Grid dimensions
GRID_SIZE = (15, 25)

# Number of robots
NUM_ROBOTS = 4

# Simulation update interval in milliseconds
STEP_INTERVAL_MS = 200

# Additional random obstacle density (on top of shelves)
RANDOM_OBSTACLE_DENSITY = 0.05

# Flask server configuration
HOST = "0.0.0.0"
PORT = 5000

# Define depot positions for each robot at the top of the grid
ROBOT_DEPOT_POSITIONS = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (0, 3),
}

