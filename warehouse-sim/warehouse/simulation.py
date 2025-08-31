import random
from .grid import Grid
from .robot import Robot
import config

class Simulation:
    """ Manages the overall simulation state and logic. """
    def __init__(self):
        self.grid = Grid(config.GRID_SIZE[0], config.GRID_SIZE[1])
        self.robots = [
            Robot(robot_id, pos, self.grid)
            for robot_id, pos in config.ROBOT_DEPOT_POSITIONS.items()
        ]
        self.tasks = []
        self.task_id_counter = 0
        self._generate_shelf_obstacles()

    def _generate_shelf_obstacles(self):
        """ Creates a structured shelf layout with a central aisle. """
        rows, cols = self.grid.rows, self.grid.cols
        center_aisle_width = 3
        side_aisle_width = 2
        
        # Calculate shelf column positions
        shelf_col1_start = side_aisle_width
        shelf_col1_end = (cols - center_aisle_width) // 2
        shelf_col2_start = shelf_col1_end + center_aisle_width
        shelf_col2_end = cols - side_aisle_width

        # Add shelf obstacles
        for r in range(2, rows - 2): # Leave top and bottom rows clear
            # Leave gaps in shelves for horizontal movement
            if r % 4 == 0: continue 
            for c in range(cols):
                if (shelf_col1_start <= c < shelf_col1_end) or \
                   (shelf_col2_start <= c < shelf_col2_end):
                    self.add_obstacle((r, c))

        # Add additional random clutter
        total_cells = rows * cols
        num_random_obs = int(total_cells * config.RANDOM_OBSTACLE_DENSITY)
        depot_positions = {pos for pos in config.ROBOT_DEPOT_POSITIONS.values()}
        
        for _ in range(num_random_obs):
            while True:
                r = random.randint(1, rows - 1) # Don't block depot lane
                c = random.randint(0, cols - 1)
                pos = (r, c)
                if pos not in depot_positions and not self.grid.is_occupied(pos):
                    self.add_obstacle(pos)
                    break

    def add_task(self, pickup, drop):
        """ Adds a new task if the locations are valid. """
        if self.grid.is_occupied(pickup) or self.grid.is_occupied(drop):
            print(f"Error: Cannot create task on an obstacle.")
            return
        task = {"id": self.task_id_counter, "pickup": pickup, "drop": drop, "status": "pending"}
        self.tasks.append(task)
        self.task_id_counter += 1
        print(f"Task {task['id']} added: Pickup {pickup}, Drop {drop}")

    def add_obstacle(self, pos):
        self.grid.add_obstacle(pos)

    def _get_all_reserved_cells(self, exclude_robot_id=None):
        """ Gathers all cells reserved by the paths of active robots. """
        reserved = set()
        for r in self.robots:
            if r.id != exclude_robot_id and r.state != "idle":
                reserved.add(r.pos)
                for pos in r.path:
                    reserved.add(pos)
        return reserved

    def _assign_tasks_and_paths(self):
        """ Assigns pending tasks to the nearest available robot that can find a path. """
        pending_tasks = [t for t in self.tasks if t['status'] == 'pending']
        available_robots = [r for r in self.robots if r.state == 'idle']

        for task in pending_tasks:
            if not available_robots: break
            
            available_robots.sort(key=lambda r: self._calculate_distance(r.pos, task['pickup']))

            for robot in available_robots:
                blocked_cells = self._get_all_reserved_cells(exclude_robot_id=robot.id)
                path_found = robot.calculate_path_for_task(task, blocked_cells)
                
                if path_found:
                    task['status'] = 'assigned'
                    available_robots.remove(robot)
                    print(f"Task {task['id']} assigned to Robot {robot.id}")
                    break

    def step(self):
        """ Executes one time step: assign tasks, then move robots. """
        self._assign_tasks_and_paths()
        for robot in self.robots:
            robot.move_step()
        self.tasks = [t for t in self.tasks if t['status'] != 'completed']

    def reset_robots(self):
        """ Resets all robots to their depot and clears all tasks. """
        print("--- END OF SHIFT: RESETTING ALL ROBOTS ---")
        for robot in self.robots:
            robot.reset()
        # Mark all non-completed tasks as pending again
        for task in self.tasks:
            if task['status'] == 'assigned':
                task['status'] = 'pending'

    def get_robot_positions(self):
        return [{"id": r.id, "pos": r.pos, "state": r.state} for r in self.robots]

    def get_task_positions(self):
        return [t for t in self.tasks if t['status'] in ['pending', 'assigned']]

    def _calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

