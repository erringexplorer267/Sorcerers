import numpy as np

class Grid:
    """ Represents the warehouse floor grid, containing only static obstacles. """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.blocked = []

    def add_obstacle(self, pos):
        """ Marks a cell as a permanent obstacle. """
        if pos not in self.blocked:
            self.blocked.append(pos)
            self.grid[pos[0], pos[1]] = -1

    def is_valid(self, pos):
        """ Checks if a position is within the grid boundaries. """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_occupied(self, pos):
        """ Checks if a cell is blocked by a permanent obstacle. """
        if not self.is_valid(pos):
            return True
        return self.grid[pos[0], pos[1]] == -1

