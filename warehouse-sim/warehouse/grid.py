import numpy as np

class Grid:
    """ Represents the warehouse floor grid. """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.blocked = []
        self.reserved_cells = {}

    def add_obstacle(self, pos):
        """ Marks a cell as a permanent obstacle. """
        if pos not in self.blocked:
            self.blocked.append(pos)
            self.grid[pos] = -1

    def is_valid(self, pos):
        """ Checks if a position is within the grid boundaries. """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_occupied(self, pos):
        """ Checks if a cell is blocked by an obstacle. """
        return self.grid[pos] == -1

    def reserve_cell(self, robot_id, pos):
        """ Allows a robot to reserve its next target cell. """
        if self.is_cell_reservable(pos):
            self.reserved_cells[pos] = robot_id
            return True
        return False

    def clear_reservation(self, pos):
        """ Clears a reservation when a robot moves out of a cell. """
        if pos in self.reserved_cells:
            del self.reserved_cells[pos]

    def is_cell_reservable(self, pos):
        """ Checks if a cell can be reserved (not an obstacle or already reserved). """
        return not self.is_occupied(pos) and pos not in self.reserved_cells
