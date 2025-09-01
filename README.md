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
├── /circuit_diagram/      → Circuit schematic & wiring images
├── /arduino_code/         → Arduino UNO sketches (.ino)
├── /python_backend/       → Flask + MongoDB integration
├── /dashboard/            → HTML, CSS, JS for dashboard
├── /presentation/         → Project PPT / PDF
├── /flowchart/            → System flowchart diagrams
└── README.md              → Project documentation
```

---

## 📸 Project Media

* 🔌 **Circuit Diagram** → ![Circuit Diagram](./circuit_diagram/\[circuit_filename].png)
* 🖥 **Dashboard Screenshot** → ![Dashboard](./dashboard/\[dashboard_filename].png)
* 📊 **Flowchart** → ![Flowchart](./flowchart/\[flowchart_filename].png)

---

## 💻 Tech Stack

### **Hardware / Simulation**

* Arduino UNO
* Motor Driver (L298N / L293D)
* LDR Sensors
* Ultrasonic Sensor
* DC Motors (prototype)

### **Software**

Python

C: Used in Arduino firmware for low-level hardware control.

Dijkstra’s Algorithm: Optimizes shortest path navigation for the robot.

KNN Mapping: For path classification and decision-making in navigation.

VS Code: Primary development environment for coding & debugging.

NumPy: Supports matrix operations, sensor data processing & calculations.

Flask: Lightweight backend for IoT dashboard and communication.

HTML, CSS, JS: Frontend interface for monitoring and controlling robot.

MongoDB: Cloud-based storage for logging paths, tasks.
<img width="905" height="576" alt="image" src="https://github.com/user-attachments/assets/289b1514-1dae-4dce-9640-9dba031d6ef1" />

### **Algorithms**

* Dijkstra’s Algorithm (pathfinding)
* KNN Mapping (navigation optimization)

---

## 🚀 Getting Started

### **1. Clone this Repository**

```bash
git clone https://github.com/your-username/Circuit-Simulator-Robot-Simulation.git
cd Circuit-Simulator-Robot-Simulation
```

### **2. Run Arduino Simulation**

* Open `[arduino_code/main.ino]` in **Arduino IDE**
* Select board: *Arduino UNO*
* Upload & simulate circuit in Tinkercad

### **3. Start Python Backend**

```bash
cd python_backend
python app.py
```

* Runs Flask server at `http://127.0.0.1:5000`

### **4. Open Dashboard**

Open `dashboard/index.html` in a browser to view monitoring system.

---

## 📑 Project Presentation

You can view the project presentation here:
👉 [Project Presentation](./presentation/[presentation_filename].pptx)

---

## 📌 Future Scope

* Integration with **ROS 2 + Gazebo** for 3D robotics simulation
* Real-time cloud storage for large-scale warehouse data
* Upgrade from DC motors → BLDC/Stepper motors for heavy payload transport
* MQTT protocol for IoT-based warehouse networking

---

## 👨‍💻 Authors

* **\[Your Name]** – Circuit Design & Simulation
* **\[Team Member]** – Backend & Dashboard Development
* **\[Team Member]** – Algorithm Design

---

⚡ *This project demonstrates how simulation-based prototypes can scale into real-world warehouse robotics solutions.*

---

Would you like me to **add shields.io badges** (like Python, Arduino, MongoDB logos, etc.) at the top of the README to make it look more professional for GitHub?
