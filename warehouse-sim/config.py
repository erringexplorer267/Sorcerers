# Grid dimensions
GRID_SIZE = (15, 25)

# Number of robots
NUM_ROBOTS = 4

STEP_INTERVAL_MS = 100

# --- Physical Robot Simulation ---
ROBOT_PACE = 3
ROBOT_SCAN_RANGE = 2
DYNAMIC_OBSTACLE_CHANCE = 0.005


SHELF_BLOCKS = [
    {"start_row": 3, "row_count": 2},
    {"start_row": 8, "row_count": 2},
]
SHELF_CENTER_AISLE_WIDTH = 3
SHELF_SIDE_PADDING = 2
RANDOM_OBSTACLE_DENSITY = 0.05


HOST = "0.0.0.0"
PORT = 5000

ROBOT_DEPOT_POSITIONS = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (0, 3),
}

