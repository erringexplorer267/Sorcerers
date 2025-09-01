# Grid dimensions
GRID_SIZE = (15, 25)

# Number of robots
NUM_ROBOTS = 4

# Simulation update interval in milliseconds
STEP_INTERVAL_MS = 100

# --- Physical Robot Simulation ---
# How many steps a robot waits before moving (1 = moves every tick, 2 = every other tick, etc.)
ROBOT_PACE = 3
# How many cells ahead the robot can "see" an unexpected obstacle
ROBOT_SCAN_RANGE = 2
# Chance (from 0.0 to 1.0) for a dynamic obstacle to appear in any given tick
DYNAMIC_OBSTACLE_CHANCE = 0.005


# --- Shelf Layout Configuration ---
SHELF_BLOCKS = [
    # First block of shelves (2 rows high)
    {"start_row": 3, "row_count": 2},
    # Second block of shelves, with a 2-row gap between them
    {"start_row": 8, "row_count": 2},
]
# How many cells wide the central aisle is
SHELF_CENTER_AISLE_WIDTH = 3
# How many cells of empty space on the left/right sides of the warehouse
SHELF_SIDE_PADDING = 2
# Additional random static obstacle density (on top of shelves)
RANDOM_OBSTACLE_DENSITY = 0.05


# --- Flask server configuration ---
HOST = "0.0.0.0"
PORT = 5000

# Define depot positions for each robot at the top of the grid
ROBOT_DEPOT_POSITIONS = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (0, 3),
}

