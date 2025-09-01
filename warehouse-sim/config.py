# Grid dimensions
GRID_SIZE = (15, 25)

# Simulation update interval in milliseconds
STEP_INTERVAL_MS = 200

# Flask server configuration
HOST = "0.0.0.0"
PORT = 5000

# Define depot positions for each robot (3 rows clear at the top)
ROBOT_DEPOT_POSITIONS = {
    0: (1, 1),
    1: (1, 2),
    2: (1, 3),
    3: (1, 4),
}

# --- Shelf Layout Configuration ---
SHELF_BLOCKS = [
    # First block of shelves (2 rows high)
    {"start_row": 4, "row_count": 2},
    # Second block of shelves (2 rows high)
    # The gap between this and the first block creates the 2-row high aisle
    {"start_row": 4 + 2 + 2, "row_count": 2},
]
# Leave 2 columns clear on the left and right sides
SHELF_SIDE_PADDING = 2
# A 2-column gap in the middle for the central vertical aisle
SHELF_CENTER_AISLE_WIDTH = 3
# Additional random obstacle density (on top of shelves)
RANDOM_OBSTACLE_DENSITY = 0.07

