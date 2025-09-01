from heapq import heappush, heappop

class Robot:
    """ Represents a single warehouse robot. """
    def __init__(self, robot_id, start_pos, grid):
        self.id = robot_id
        self.start_pos = start_pos  # The robot's home depot position
        self.pos = start_pos
        self.grid = grid
        self.path = []
        self.task = None
        # States: idle, moving_to_pickup, moving_to_drop, returning
        self.state = "idle"

    def calculate_path_for_task(self, task, blocked_cells):
        """
        Calculates a full path for a task, considering blocked cells.
        Returns True if a path was found, False otherwise.
        """
        path_to_pickup = self._dijkstra(self.pos, task['pickup'], blocked_cells)
        if not path_to_pickup:
            return False

        # --- BUG FIX ---
        # When calculating the second leg of the journey, the pickup cell must be a valid
        # starting point, so we add the pickup path EXCEPT for the destination cell itself.
        newly_blocked = blocked_cells.union(set(path_to_pickup[:-1]))
        path_to_drop = self._dijkstra(task['pickup'], task['drop'], newly_blocked)
        if not path_to_drop:
            return False

        # Path found, assign it to the robot
        self.path = path_to_pickup + path_to_drop[1:]
        self.task = task
        self.state = "moving_to_pickup"
        return True

    def calculate_return_path(self, blocked_cells):
        """ Calculates a path back to the robot's starting depot. """
        path_to_depot = self._dijkstra(self.pos, self.start_pos, blocked_cells)
        if path_to_depot:
            self.path = path_to_depot
            self.state = "returning"
            return True
        return False

    def move_step(self):
        """ Moves the robot one step along its pre-calculated path. """
        if not self.path:
            return

        self.pos = self.path.pop(0)

        # --- State Transitions ---
        if self.state == 'moving_to_pickup' and self.pos == self.task['pickup']:
            self.state = "moving_to_drop"
        elif self.state == 'moving_to_drop' and self.pos == self.task['drop']:
            print(f"Robot {self.id} completed task {self.task['id']} at {self.pos}.")
            self.task['status'] = 'completed'
            self.task = None
            self.state = "idle" # Become idle at the drop-off location
        elif self.state == 'returning' and self.pos == self.start_pos:
            self.state = 'idle'
            print(f"Robot {self.id} has returned to depot.")


    def _dijkstra(self, start, goal, blocked_cells=None):
        """
        Dijkstra's algorithm for finding the shortest path.
        """
        if blocked_cells is None:
            blocked_cells = set()

        visited = set()
        # Heap stores: (cost, current_position, path_list)
        heap = [(0, start, [start])]

        while heap:
            cost, current, path = heappop(heap)
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)

            r, c = current
            # Cardinal directions only (no diagonals)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (r + dr, c + dc)
                if self.grid.is_valid(next_pos) and \
                   not self.grid.is_occupied(next_pos) and \
                   next_pos not in blocked_cells:
                    heappush(heap, (cost + 1, next_pos, path + [next_pos]))
        return [] # No path found

