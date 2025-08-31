from heapq import heappush, heappop

class Robot:
    """ Represents a single warehouse robot. """
    def __init__(self, robot_id, start_pos, grid):
        self.id = robot_id
        self.pos = start_pos
        self.grid = grid
        self.path = []
        self.task = None
        self.state = "idle"

    def assign_task(self, task):
        """ Assigns a task and calculates the full path from current pos -> pickup -> drop. """
        self.task = task
        self.state = "moving_to_pickup"
        path_to_pickup = self._dijkstra(self.pos, self.task['pickup'])
        path_to_drop = self._dijkstra(self.task['pickup'], self.task['drop'])

        if path_to_pickup and path_to_drop:
            self.path = path_to_pickup + path_to_drop[1:]
        else:
            print(f"Robot {self.id}: Cannot find path for task {self.task}")
            self.state = "idle"
            self.task = None


    def move_step(self, other_robots):
        """
        Moves the robot one step along its path, handling state transitions
        and basic collision avoidance.
        """
        if not self.path:
            if self.state != "idle":
                self.state = "idle"
                self.task = None
            return

        next_pos = self.path[0]

        is_occupied_by_other = any(r.pos == next_pos for r in other_robots if r.id != self.id)
        is_reserved = self.grid.is_cell_reservable(next_pos) is False and self.grid.reserved_cells.get(next_pos) != self.id


        if is_occupied_by_other or is_reserved:
            print(f"Robot {self.id}: Collision detected at {next_pos}. Waiting.")
            return

        if self.grid.reserve_cell(self.id, next_pos):
            self.grid.clear_reservation(self.pos)
            self.pos = self.path.pop(0)

            if self.pos == self.task['pickup']:
                self.state = "moving_to_drop"
            elif self.pos == self.task['drop']:
                print(f"Robot {self.id} completed task {self.task['id']}.")
                self.state = "idle"
                self.task = None
                self.path = []


    def _dijkstra(self, start, goal, blocked_cells=None):
        """
        Dijkstra's algorithm for finding the shortest path.
        Considers permanent obstacles and temporarily blocked cells (other robots).
        """
        if blocked_cells is None:
            blocked_cells = set()
        else:
            blocked_cells = set(blocked_cells)

        rows, cols = self.grid.rows, self.grid.cols
        visited = set()
        heap = [(0, start, [start])]

        while heap:
            cost, current, path = heappop(heap)

            if current == goal:
                return path

            if current in visited:
                continue
            visited.add(current)

            r, c = current
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (r + dr, c + dc)
                if self.grid.is_valid(next_pos) and not self.grid.is_occupied(next_pos) and next_pos not in blocked_cells:
                    heappush(heap, (cost + 1, next_pos, path + [next_pos]))
        return []
