class Grid:
    """ Represents the warehouse floor grid and static obstacles. """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.blocked = set()  # Using a set for efficient O(1) lookups
        self.robots = [] # A reference to all robot objects

    def add_obstacle(self, pos):
        """ Adds a permanent obstacle to the grid. """
        self.blocked.add(pos)

    def is_valid(self, pos):
        """ Checks if a position is within the grid boundaries. """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_occupied(self, pos):
        """ Checks if a cell is blocked by a permanent obstacle. """
        return pos in self.blocked

    def get_all_robot_positions(self, exclude_robot_id=None):
        """ Returns a set of all current robot positions. """
        positions = set()
        for r in self.robots:
            if r.id != exclude_robot_id:
                positions.add(r.pos)
        return positions

    def is_robot_at(self, pos, querying_robot_id):
        """ Checks if another robot is at the given position. """
        for r in self.robots:
            if r.id != querying_robot_id and r.pos == pos:
                return True
        return False

