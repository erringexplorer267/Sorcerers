import random
from .grid import Grid
from .robot import Robot
import config

class Simulation:
    """ Manages the overall simulation state, robots, and tasks, including dynamic obstacles. """
    def __init__(self):
        self.grid = Grid(config.GRID_SIZE[0], config.GRID_SIZE[1])
        self.robots = [
            Robot(robot_id, pos, self.grid)
            for robot_id, pos in config.ROBOT_DEPOT_POSITIONS.items()
        ]
        self.grid.robots = self.robots
        self.tasks = []
        self.task_id_counter = 0
        self.is_shift_ending = False
        # --- FIX: Restore the dynamic_obstacles attribute ---
        self.dynamic_obstacles = set() 
        self._generate_shelf_obstacles()

    def _generate_shelf_obstacles(self):
        """ Creates a precise, structured shelf layout based on the config file. """
        rows, cols = self.grid.rows, self.grid.cols
        center_aisle_start = (cols - config.SHELF_CENTER_AISLE_WIDTH) // 2
        center_aisle_end = center_aisle_start + config.SHELF_CENTER_AISLE_WIDTH
        shelf_cols_left_start = config.SHELF_SIDE_PADDING
        shelf_cols_left_end = center_aisle_start
        shelf_cols_right_start = center_aisle_end
        shelf_cols_right_end = cols - config.SHELF_SIDE_PADDING

        for shelf_block in config.SHELF_BLOCKS:
            for r in range(shelf_block["start_row"], shelf_block["start_row"] + shelf_block["row_count"]):
                for c in range(cols):
                    is_in_left_cols = shelf_cols_left_start <= c < shelf_cols_left_end
                    is_in_right_cols = shelf_cols_right_start <= c < shelf_cols_right_end
                    if is_in_left_cols or is_in_right_cols:
                        self.grid.add_obstacle((r, c))
        self._add_random_clutter()

    def _add_random_clutter(self):
        """Adds a small percentage of random obstacles to the grid."""
        rows, cols = self.grid.rows, self.grid.cols
        total_cells = rows * cols
        num_random_obs = int(total_cells * config.RANDOM_OBSTACLE_DENSITY)
        depot_positions = set(config.ROBOT_DEPOT_POSITIONS.values())
        
        for _ in range(num_random_obs):
            attempts = 0
            while attempts < 100:
                r = random.randint(config.SHELF_BLOCKS[0]["start_row"], rows - 1)
                c = random.randint(0, cols - 1)
                pos = (r, c)
                if pos not in depot_positions and not self.grid.is_occupied(pos):
                    self.grid.add_obstacle(pos)
                    break
                attempts += 1

    def _update_dynamic_obstacles(self):
        """ Randomly creates or removes temporary obstacles to simulate a dynamic environment. """
        # Chance to remove an existing obstacle
        if self.dynamic_obstacles and random.random() < 0.1: # 10% chance to clear one
             self.dynamic_obstacles.pop()

        # Chance to add a new one
        if random.random() < config.DYNAMIC_OBSTACLE_CHANCE:
            rows, cols = self.grid.rows, self.grid.cols
            for _ in range(10): # Try 10 times to find a valid spot
                r, c = random.randint(1, rows - 2), random.randint(1, cols - 2)
                pos = (r, c)
                if not self.grid.is_occupied(pos) and pos not in self.dynamic_obstacles:
                    self.dynamic_obstacles.add(pos)
                    self.grid.dynamic_obstacles.add(pos)
                    break

    def add_task(self, pickup, drop):
        """ Adds a new task if the locations are valid. """
        if self.is_shift_ending:
            print("Cannot add tasks while shift is ending.")
            return
        if self.grid.is_occupied(pickup) or self.grid.is_occupied(drop):
            print(f"Error: Cannot create task on an obstacle.")
            return
        task = {"id": self.task_id_counter, "pickup": pickup, "drop": drop, "status": "pending"}
        self.tasks.append(task)
        self.task_id_counter += 1
        print(f"Task {task['id']} added: Pickup {pickup}, Drop {drop}")

    def _get_active_path_reservations(self, exclude_robot_id=None):
        """ Gathers cells reserved by other ACTIVE (non-idle) robots. """
        reserved = set()
        for r in self.robots:
            if r.id != exclude_robot_id and r.state != "idle":
                reserved.add(r.pos)
                reserved.update(r.path)
        return reserved

    def _assign_tasks(self):
        """ Assigns pending tasks to the robot with the shortest ACTUAL path. """
        pending_tasks = [t for t in self.tasks if t['status'] == 'pending']
        if not pending_tasks: return

        for task in pending_tasks:
            idle_robots = [r for r in self.robots if r.state == 'idle']
            if not idle_robots: break
            
            potential_assignments = []
            for robot in idle_robots:
                blocked_for_check = self._get_active_path_reservations(exclude_robot_id=robot.id)
                path_to_pickup = robot._dijkstra(robot.pos, task['pickup'], blocked_for_check)
                
                if path_to_pickup:
                    potential_assignments.append((len(path_to_pickup), robot))

            if not potential_assignments:
                print(f"Task {task['id']} at {task['pickup']} is temporarily blocked. Waiting...")
                continue

            potential_assignments.sort(key=lambda x: x[0])
            best_path_len, best_robot = potential_assignments[0]

            blocked_cells = self._get_active_path_reservations(exclude_robot_id=best_robot.id)
            if best_robot.calculate_path_for_task(task, blocked_cells):
                task['status'] = 'assigned'
                print(f"Task {task['id']} assigned to Robot {best_robot.id} (True path distance: {best_path_len})")

    def _handle_returns(self):
        """ Manages the concurrent and collision-free return of all robots. """
        if all(r.pos == r.start_pos and r.state == 'idle' for r in self.robots):
            self.is_shift_ending = False
            self.tasks.clear()
            print("--- All robots have returned. Shift ended. ---")
            return

        currently_reserved = self._get_active_path_reservations()
        robots_to_dispatch = sorted(
            [r for r in self.robots if r.state != 'returning' and r.pos != r.start_pos],
            key=lambda r: r.id
        )

        for robot in robots_to_dispatch:
            path_found = robot.calculate_return_path(currently_reserved)
            if path_found:
                currently_reserved.update(robot.path)

    def step(self):
        """ Executes one time step of the simulation. """
        self._update_dynamic_obstacles()
        if self.is_shift_ending:
            self._handle_returns()
        else:
            self._assign_tasks()
        
        for robot in self.robots:
            robot.move_step()
        
        self.tasks = [t for t in self.tasks if t['status'] != 'completed']

    def initiate_shift_end(self):
        """ Starts the process of ending the shift. """
        if self.is_shift_ending: return
        print("--- END OF SHIFT INITIATED ---")
        self.is_shift_ending = True
        
        for task in self.tasks:
            if task['status'] in ['pending', 'assigned']:
                task['status'] = 'cancelled'
        
        for robot in self.robots:
            robot.task = None

    def get_robot_data(self):
        """ Returns data for all robots, including their next intended move. """
        robot_data = []
        for r in self.robots:
            next_pos = r.path[0] if r.path else None
            robot_data.append({"id": r.id, "pos": r.pos, "state": r.state, "next_pos": next_pos})
        return robot_data

    def get_task_positions(self):
        return [t for t in self.tasks if t['status'] in ['pending', 'assigned']]

