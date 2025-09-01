**🚗 Circuit Simulator Robot Simulation Project**

## 📌 Overview

This repository contains the complete implementation of a **Robot Simulation** designed as a warehouse-assist prototype.
The project integrates:

* **Circuit simulation in Tinkercad**
* **Arduino + Sensors (LDR, Ultrasonic, Motor Driver)**
* **Python-based database & backend**
* **Local hosted prototype dashboard**
* **Flowchart + Project Presentation**

The simulation mimics a line-following + obstacle-detection robot with scalability for warehouse automation.

---

## 🛠️ Features

* ✅ Line-following using LDR sensors
* ✅ Obstacle detection via Ultrasonic sensor
* ✅ Control logic using Arduino UNO
* ✅ Local Flask-based dashboard for monitoring
* ✅ Data logging with MongoDB
* ✅ Pathfinding concepts with **Dijkstra’s Algorithm** + **KNN Mapping**

---

## 📂 Repository Structure

```
📦 Circuit-Simulator-Robot-Simulation
├── Circuit Simulation.png/      → Circuit schematic & wiring images
├── arduino_code/                → Arduino UNO sketches (.ino)
├── warehouse-sim/│
│    ├── app.py                      # Main Flask application file. Runs the web server and simulation.
│    ├── config.py                   # Central configuration for grid size, robots, layout, etc.
│    ├── requirements.txt            # Lists the Python dependencies for the project.
│    │
│    ├── static/
│    │   ├── script.js               # Frontend JavaScript for UI interaction and fetching updates.
│    │   └── style.css               # CSS for styling the web dashboard.
│    │
│    ├── templates/
│    │   └── index.html              # The main HTML file for the web interface.
│    │
│    └── warehouse/
│    │   ├── __init__.py             # Makes the 'warehouse' directory a Python package.
│    │   ├── grid.py                 # Defines the Grid class, managing static obstacles.
│    │   ├── robot.py                # Defines the Robot class, including its movement and pathfinding logic.
│    │   └── simulation.py           # The core simulation engine that manages all robots, tasks, and the main loop.
├── Sorcerers.pptx/              → Project PPT / PDF
├── Flow.png/                    → System flowchart diagrams
└── README.md                    → Project documentation
```

---


## 💻 Tech Stack

### **Hardware / Simulation**

* Arduino UNO
* Motor Driver (L298N / L293D)
* LDR Sensors
* Ultrasonic Sensor
* DC Motors (prototype)

### **Software**

### Python

### C:
 Used in Arduino firmware for low-level hardware control.

### Dijkstra’s Algorithm: 
Optimizes shortest path navigation for the robot.

### KNN Mapping:
 For path classification and decision-making in navigation.

### VS Code:
 Primary development environment for coding & debugging.

### NumPy:
 Supports matrix operations, sensor data processing & calculations.

### Flask: 
Lightweight backend for IoT dashboard and communication.

### HTML, CSS, JS: 
Frontend interface for monitoring and controlling robot.

### **Algorithms**

* Dijkstra’s Algorithm (pathfinding)
* KNN Mapping (navigation optimization)

---

## 🚀 Getting Started

### **1. Clone this Repository**

```bash
git clone https://github.com/erringexplorer267/Sorcerers.git
```
```python
cd warehouse-sim
```

### **2. Run Arduino Simulation**

* Open `[arduino_code/main.ino]` in **Arduino IDE**
* Select board: *Arduino UNO*
* Upload & simulate circuit in Tinkercad

### **3. Start Python Backend**

```bash
cd warehouse-sim
```
```python
pip install -r requirements.txt
```
```bash
python app.py
```

* Runs Flask server at `http://127.0.0.1:5000`

### **4. Open Dashboard**

Open `http://127.0.0.1:5000` in a browser to view monitoring system.

---

## 📑 Project Presentation

You can view the project presentation here:
👉 [Project Presentation](./presentation/Sorcerers.pptx)

---

## 📌 Future Scope

* Integration with **ROS 2 + Gazebo** for 3D robotics simulation
* Real-time cloud storage for large-scale warehouse data on MongoDB
* Upgrade from DC motors → BLDC/Stepper motors for heavy payload transport
* MQTT protocol for IoT-based warehouse networking

---

## 👨‍💻 Authors

* **Uttiyo Modak** – Circuit Design & Simulation
* **Tanushree Das** – Content maker
* **Suman Chakraborty** – Videography
* **Subhabrata Mondal** – Backend & Dashboard Development


---

>⚡ *This project demonstrates how simulation-based prototypes can scale into real-world warehouse robotics solutions.*

---
