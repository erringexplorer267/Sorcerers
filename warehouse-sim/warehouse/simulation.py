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
            for robot_id, pos in config.ROBOT_START_POSITIONS.items()
        ]
        self.tasks = []
        self.task_id_counter = 0
        self._generate_random_obstacles()

    def _generate_random_obstacles(self):
        """ Fills the grid with a set density of random obstacles. """
        total_cells = self.grid.rows * self.grid.cols
        num_obstacles = int(total_cells * config.OBSTACLE_DENSITY)
        start_positions = {pos for pos in config.ROBOT_START_POSITIONS.values()}

        for _ in range(num_obstacles):
            while True:
                r = random.randint(0, self.grid.rows - 1)
                c = random.randint(0, self.grid.cols - 1)
                pos = (r, c)
                if pos not in start_positions and not self.grid.is_occupied(pos):
                    self.add_obstacle(pos)
                    break

    def add_task(self, pickup, drop):
        """ Adds a new task if the locations are not obstacles. """
        if self.grid.is_occupied(pickup) or self.grid.is_occupied(drop):
            print(f"Error: Cannot create task on an obstacle at {pickup} or {drop}.")
            return

        task = {"id": self.task_id_counter, "pickup": pickup, "drop": drop, "status": "pending"}
        self.tasks.append(task)
        self.task_id_counter += 1
        print(f"Task {task['id']} added: Pickup {pickup}, Drop {drop}")

    def add_obstacle(self, pos):
        """ Adds a permanent obstacle to the grid. """
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
        """
        Assigns pending tasks and calculates conflict-free paths.
        This is the core logic to prevent deadlocks.
        """
        returning_robots = [r for r in self.robots if r.state == 'returning' and not r.path]
        for robot in returning_robots:
             blocked_cells = self._get_all_reserved_cells(exclude_robot_id=robot.id)
             path_home = robot._dijkstra(robot.pos, robot.start_pos, blocked_cells)
             if path_home:
                 robot.path = path_home
                 print(f"Robot {robot.id} path home calculated.")
             else:
                 print(f"Robot {robot.id} cannot find path home. Waiting.")


        pending_tasks = [t for t in self.tasks if t['status'] == 'pending']
        available_robots = [r for r in self.robots if r.state == 'idle']

        for task in pending_tasks:
            if not available_robots:
                break

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
        """ Executes a single time step in the simulation. """
        self._assign_tasks_and_paths()
        for robot in self.robots:
            robot.move_step()
        self.tasks = [t for t in self.tasks if t['status'] != 'completed']

    def get_robot_positions(self):
        return [{"id": r.id, "pos": r.pos, "state": r.state} for r in self.robots]

    def get_task_positions(self):
        return [t for t in self.tasks if t['status'] in ['pending', 'assigned']]

    def _calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

