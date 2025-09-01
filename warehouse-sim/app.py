from flask import Flask, render_template, request, jsonify
from warehouse.simulation import Simulation
import config

app = Flask(__name__)
# Create a single simulation instance
sim = Simulation()

@app.route('/')
def index():
    """ Renders the main dashboard page. """
    return render_template('index.html')

@app.route('/init', methods=['GET'])
def init_sim():
    """ 
    Provides initial simulation state to the frontend on page load.
    """
    return jsonify({
        "grid_size": config.GRID_SIZE,
        "robot_data": sim.get_robot_data(),
        # --- ROBUST FIX: Explicitly convert all collections to lists ---
        "obstacles": list(sim.grid.blocked), 
        "dynamic_obstacles": list(sim.dynamic_obstacles), 
        "step_interval": config.STEP_INTERVAL_MS,
    })

@app.route('/add_task', methods=['POST'])
def add_task():
    """ Adds a new pickup-and-drop task to the simulation. """
    data = request.json
    pickup = tuple(data['pickup'])
    drop = tuple(data['drop'])
    sim.add_task(pickup, drop)
    return jsonify({"status": "success", "message": "Task added."})

@app.route('/update', methods=['GET'])
def update_sim():
    """
    Executes one simulation step and returns the current state.
    This is polled by the frontend to create the animation.
    """
    sim.step()
    return jsonify({
        "robot_data": sim.get_robot_data(),
        "tasks": sim.get_task_positions(),
        # --- ROBUST FIX: Explicitly convert all collections to lists ---
        "dynamic_obstacles": list(sim.dynamic_obstacles)
    })

@app.route('/reset_shift', methods=['POST'])
def reset_shift():
    """ Starts the process of returning all robots to their depots. """
    sim.initiate_shift_end()
    return jsonify({"status": "success", "message": "Shift end initiated. Robots are returning to depot."})


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)

