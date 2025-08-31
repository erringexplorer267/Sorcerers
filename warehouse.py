import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Grid size
GRID_ROWS = 10
GRID_COLS = 10
STEP_COUNT = 20

# Define 4 robots with random paths
class Robot:
    def __init__(self, start):
        self.path = [start]
        self.blocked_cells = []

# Create robots with random walks
robots = [
    Robot([0, 0]),
    Robot([0, 9]),
    Robot([9, 0]),
    Robot([9, 9])
]

# Generate random paths for demo
np.random.seed(42)
for r in robots:
    for _ in range(STEP_COUNT-1):
        last = r.path[-1]
        move = last + np.random.choice([-1, 0, 1], size=2)
        move[0] = np.clip(move[0], 0, GRID_ROWS-1)
        move[1] = np.clip(move[1], 0, GRID_COLS-1)
        r.path.append(move)
        # Randomly mark some blocked cells
        if np.random.rand() < 0.2:
            r.blocked_cells.append(move)

# Plot setup
fig, ax = plt.subplots()
ax.set_xlim(-0.5, GRID_COLS-0.5)
ax.set_ylim(-0.5, GRID_ROWS-0.5)
ax.set_xticks(range(GRID_COLS))
ax.set_yticks(range(GRID_ROWS))
ax.grid(True)

# Create robot markers
colors = ['r', 'g', 'b', 'm']
markers = [ax.plot([], [], 'o', color=colors[i])[0] for i in range(len(robots))]

# Scatter for blocked cells
blocked_plot = ax.scatter([], [], marker='s', color='k', s=100)

# Animation functions
def init():
    for m in markers:
        m.set_data([], [])
    blocked_plot.set_offsets(np.empty((0,2)))
    return markers + [blocked_plot]

def animate(step):
    for i, robot in enumerate(robots):
        pos = robot.path[step] if step < len(robot.path) else robot.path[-1]
        markers[i].set_data([pos[1]], [pos[0]])  # wrap in list

    # Update blocked cells
    blocked_positions = [cell for r in robots for cell in r.blocked_cells if step < len(r.blocked_cells)]
    if blocked_positions:
        blocked_array = np.array([[c[1], c[0]] for c in blocked_positions])
        blocked_plot.set_offsets(blocked_array)
    else:
        blocked_plot.set_offsets(np.empty((0, 2)))

    return markers + [blocked_plot]

# Animate
ani = animation.FuncAnimation(fig, animate, frames=STEP_COUNT,
                              init_func=init, interval=500, blit=True)

plt.show()
