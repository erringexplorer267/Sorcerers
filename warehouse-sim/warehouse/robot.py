from heapq import heappush, heappop

class Robot:
    """ Represents a single warehouse robot. """
    def __init__(self, robot_id, start_pos, grid):
        self.id = robot_id
        self.start_pos = start_pos
        self.pos = start_pos
        self.grid = grid
        self.path = []
        self.task = None
        # States: idle, moving_to_pickup, moving_to_drop, returning
        self.state = "idle"

    def calculate_path_for_task(self, task, blocked_cells):
        """
        Calculates a full path for a task, considering blocked cells, and sets it.
        Returns True if a path was found, False otherwise.
        """
        path_to_pickup = self._dijkstra(self.pos, task['pickup'], blocked_cells)
        if not path_to_pickup:
            return False

        newly_blocked = blocked_cells.union(set(path_to_pickup))
        path_to_drop = self._dijkstra(task['pickup'], task['drop'], newly_blocked)
        if not path_to_drop:
            return False

        self.path = path_to_pickup + path_to_drop[1:]
        self.task = task
        self.state = "moving_to_pickup"
        return True

    def move_step(self):
        """
        Moves the robot one step along its pre-calculated path.
        No collision checks are needed here as paths are guaranteed to be conflict-free.
        """
        if not self.path:
            if self.state == "returning" and self.pos == self.start_pos:
                print(f"Robot {self.id} has returned to start and is now idle.")
                self.state = "idle"
            return

        self.pos = self.path.pop(0)

        if self.task and self.state == 'moving_to_pickup' and self.pos == self.task['pickup']:
            self.state = "moving_to_drop"
        elif self.task and self.state == 'moving_to_drop' and self.pos == self.task['drop']:
            print(f"Robot {self.id} completed task {self.task['id']}.")
            self.task['status'] = 'completed'
            self.task = None
            self.state = "returning"
            self.path = []


    def _dijkstra(self, start, goal, blocked_cells=None):
        """
        Dijkstra's algorithm for finding the shortest path.
        Considers permanent obstacles and temporarily blocked cells (other robot paths).
        """
        if blocked_cells is None:
            blocked_cells = set()

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

