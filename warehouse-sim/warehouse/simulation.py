from .grid import Grid
from .robot import Robot
import config
import math

class Simulation:
    """ Manages the overall simulation state and logic. """
    def __init__(self):
        self.grid = Grid(config.GRID_SIZE[0], config.GRID_SIZE[1])
        self.robots = [Robot(i, (0, i), self.grid) for i in range(config.NUM_ROBOTS)]
        self.tasks = []
        self.task_id_counter = 0

    def add_task(self, pickup, drop):
        """ Adds a new task to the queue. """
        task = {
            "id": self.task_id_counter,
            "pickup": pickup,
            "drop": drop,
            "status": "pending"
        }
        self.tasks.append(task)
        self.task_id_counter += 1
        print(f"Task {task['id']} added: Pickup {pickup}, Drop {drop}")

    def _assign_task_to_robot(self):
        """ Assigns pending tasks to the nearest idle robot. """
        pending_tasks = [t for t in self.tasks if t['status'] == 'pending']
        idle_robots = [r for r in self.robots if r.state == 'idle']

        for task in pending_tasks:
            if not idle_robots:
                break 

            best_robot = None
            min_dist = float('inf')
            for robot in idle_robots:
                dist = self._calculate_distance(robot.pos, task['pickup'])
                if dist < min_dist:
                    min_dist = dist
                    best_robot = robot

            if best_robot:
                task['status'] = 'assigned'
                best_robot.assign_task(task)
                idle_robots.remove(best_robot)
                print(f"Task {task['id']} assigned to Robot {best_robot.id}")


    def step(self):
        """
        Executes a single time step in the simulation.
        1. Assigns any pending tasks.
        2. Moves each robot one step.
        """
        self._assign_task_to_robot()

        # Create a list of other robots for collision avoidance check
        for robot in self.robots:
            other_robots = [r for r in self.robots if r.id != robot.id]
            robot.move_step(other_robots)

        self.tasks = [t for t in self.tasks if t['status'] != 'completed']


    def get_robot_positions(self):
        """ Returns the current positions of all robots and their state. """
        return [{"id": r.id, "pos": r.pos, "state": r.state} for r in self.robots]

    def get_task_positions(self):
        """ Returns the locations of all active tasks. """
        return [
            {"id": t['id'], "pickup": t['pickup'], "drop": t['drop'], "status": t['status']}
            for t in self.tasks if t['status'] in ['pending', 'assigned']
        ]

    def _calculate_distance(self, pos1, pos2):
        """ Calculates Manhattan distance between two points. """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
