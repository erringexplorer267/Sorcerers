from flask import Flask, render_template, request, jsonify
from warehouse.simulation import Simulation
import config

app = Flask(__name__)
sim = Simulation()

@app.route('/')
def index():
    """ Renders the main dashboard page. """
    return render_template('index.html')

@app.route('/init', methods=['GET'])
def init_sim():
    """ Provides initial simulation state to the frontend. """
    return jsonify({
        "grid_size": config.GRID_SIZE,
        "robot_positions": sim.get_robot_positions(),
        "obstacles": sim.grid.blocked
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
        "robot_positions": sim.get_robot_positions(),
        "tasks": sim.get_task_positions()
    })

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)
