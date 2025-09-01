from heapq import heappush, heappop
import config

class Robot:
    """ Represents a single warehouse robot with simulated sensors. """
    def __init__(self, robot_id, start_pos, grid):
        self.id = robot_id
        self.start_pos = start_pos
        self.pos = start_pos
        self.grid = grid
        self.path = []
        self.task = None
        self.state = "idle" # idle, moving_to_pickup, moving_to_drop, returning
        
        # --- Simulated Physical Attributes ---
        self.pace_counter = 0 
        # Memory of temporary obstacles seen by its "sensors"
        self.temp_obstacles = set()

    def calculate_path_for_task(self, task, blocked_cells):
        """ Calculates a full path for a task, considering all known obstacles. """
        self.temp_obstacles.clear() # Clear memory of old dynamic obstacles
        
        blocked_with_temp = blocked_cells.union(self.temp_obstacles)
        path_to_pickup = self._dijkstra(self.pos, task['pickup'], blocked_with_temp)
        if not path_to_pickup:
            return False

        newly_blocked = blocked_with_temp.union(set(path_to_pickup[:-1]))
        path_to_drop = self._dijkstra(task['pickup'], task['drop'], newly_blocked)
        if not path_to_drop:
            return False

        self.path = path_to_pickup + path_to_drop[1:]
        self.task = task
        self.state = "moving_to_pickup"
        return True

    def calculate_return_path(self, blocked_cells):
        """ Calculates a path back to the depot. """
        self.temp_obstacles.clear()
        path_to_depot = self._dijkstra(self.pos, self.start_pos, blocked_cells)
        if path_to_depot:
            self.path = path_to_depot
            self.state = "returning"
            return True
        return False

    def scan_and_react(self, dynamic_obstacles, other_robot_paths):
        """
        Simulates a sensor scan. If an obstacle is detected, it triggers a path recalculation.
        Returns True if a recalculation happened, False otherwise.
        """
        if self.state == 'idle': return False

        scan_path = self.path[:config.ROBOT_SCAN_RANGE]
        for cell in scan_path:
            if cell in dynamic_obstacles:
                print(f"Robot {self.id} detected dynamic obstacle at {cell}! Re-routing...")
                self.temp_obstacles.add(cell) # Add to its personal memory of hazards
                
                # The robot must re-plan its entire current objective
                all_blocked = self.temp_obstacles.union(other_robot_paths)
                
                if self.state == 'moving_to_pickup' or self.state == 'moving_to_drop':
                    self.calculate_path_for_task(self.task, all_blocked)
                elif self.state == 'returning':
                    self.calculate_return_path(all_blocked)
                
                return True # Path was recalculated
        return False

    def move_step(self):
        """ 
        Moves the robot one step along its path, but only if its pace counter allows it.
        This simulates the speed of a physical robot.
        """
        self.pace_counter += 1
        if self.pace_counter < config.ROBOT_PACE:
            return

        if not self.path:
            return
        
        self.pace_counter = 0 # Reset counter after moving
        self.pos = self.path.pop(0)

        # --- State Transitions ---
        if self.task and self.state == 'moving_to_pickup' and self.pos == self.task['pickup']:
            self.state = "moving_to_drop"
        elif self.task and self.state == 'moving_to_drop' and self.pos == self.task['drop']:
            print(f"Robot {self.id} completed task {self.task['id']} at {self.pos}.")
            self.task['status'] = 'completed'
            self.task = None
            self.state = "idle"
        elif self.state == 'returning' and self.pos == self.start_pos:
            self.state = 'idle'
            print(f"Robot {self.id} has returned to depot.")


    def _dijkstra(self, start, goal, blocked_cells=None):
        """ Dijkstra's algorithm for finding the shortest path. """
        if blocked_cells is None: blocked_cells = set()
        visited = set()
        heap = [(0, start, [start])]
        while heap:
            cost, current, path = heappop(heap)
            if current == goal: return path
            if current in visited: continue
            visited.add(current)
            r, c = current
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (r + dr, c + dc)
                if self.grid.is_valid(next_pos) and \
                   not self.grid.is_occupied(next_pos) and \
                   next_pos not in blocked_cells:
                    heappush(heap, (cost + 1, next_pos, path + [next_pos]))
        return []

