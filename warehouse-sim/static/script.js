document.addEventListener('DOMContentLoaded', () => {
    // --- UI Element References ---
    const gridDiv = document.getElementById('grid');
    const createTaskBtn = document.getElementById('create-task-btn');
    const clearSelectionBtn = document.getElementById('clear-selection-btn');
    const resetShiftBtn = document.getElementById('reset-shift-btn');
    const pickupPosSpan = document.getElementById('pickup-pos');
    const dropPosSpan = document.getElementById('drop-pos');

    // --- State Variables ---
    let gridRows = 0;
    let gridCols = 0;
    let selectedPickup = null;
    let selectedDrop = null;
    let static_obstacles = [];

    // --- Initialization ---
    async function initialize() {
        try {
            const response = await fetch('/init');
            if (!response.ok) { // Check for server errors
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            gridRows = data.grid_size[0];
            gridCols = data.grid_size[1];
            static_obstacles = data.obstacles;
            createGrid();
            // --- FIX: Use 'robot_data' key and handle initial dynamic obstacles ---
            updateGrid(data.robot_data, [], data.dynamic_obstacles || []);
            setInterval(mainLoop, data.step_interval || 200);
        } catch (error) {
            console.error("Initialization failed:", error);
            gridDiv.innerHTML = "<p>Error connecting to the simulation server. Please try refreshing.</p>";
        }
    }

    // --- Main Simulation Loop ---
    async function mainLoop() {
        try {
            const response = await fetch('/update');
             if (!response.ok) {
                console.error(`HTTP error! status: ${response.status}`);
                return;
            }
            const data = await response.json();
            updateGrid(data.robot_data, data.tasks, data.dynamic_obstacles);
        } catch (error) {
            console.error("Error fetching update:", error);
        }
    }

    // --- Grid UI Management ---
    function createGrid() {
        gridDiv.innerHTML = '';
        gridDiv.style.setProperty('--grid-rows', gridRows);
        gridDiv.style.setProperty('--grid-cols', gridCols);
        for (let r = 0; r < gridRows; r++) {
            for (let c = 0; c < gridCols; c++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.id = `cell-${r}-${c}`;
                cell.dataset.row = r;
                cell.dataset.col = c;
                cell.addEventListener('click', onCellClick);
                gridDiv.appendChild(cell);
            }
        }
    }

    function updateGrid(robots, tasks, dynamic_obstacles) {
        // Clear previous state
        document.querySelectorAll('.cell').forEach(cell => {
            cell.className = 'cell';
            cell.textContent = '';
        });

        // Draw static obstacles
        static_obstacles.forEach(obs => {
             document.getElementById(`cell-${obs[0]}-${obs[1]}`)?.classList.add('obstacle');
        });
        
        // Draw dynamic obstacles
        dynamic_obstacles.forEach(obs => {
            document.getElementById(`cell-${obs[0]}-${obs[1]}`)?.classList.add('dynamic-obstacle');
        });

        // Draw tasks
        tasks.forEach(task => {
            document.getElementById(`cell-${task.pickup[0]}-${task.pickup[1]}`)?.classList.add('task-pickup');
            document.getElementById(`cell-${task.drop[0]}-${task.drop[1]}`)?.classList.add('task-drop');
        });

        // Draw robots and their next intended move
        robots.forEach(robot => {
            const currentCell = document.getElementById(`cell-${robot.pos[0]}-${robot.pos[1]}`);
            if (currentCell) {
                currentCell.classList.add('robot', `robot-${robot.state}`);
                currentCell.textContent = `R${robot.id}`;
            }
            if (robot.next_pos) {
                const nextCell = document.getElementById(`cell-${robot.next_pos[0]}-${robot.next_pos[1]}`);
                if (nextCell) {
                    nextCell.classList.add('next-move', `robot-${robot.state}-next`);
                }
            }
        });
    }

    // --- User Interaction ---
    function onCellClick(event) {
        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);

        if (event.target.classList.contains('obstacle') || event.target.classList.contains('robot')) {
            console.warn("Cannot select an obstacle or robot cell.");
            return;
        }

        if (!selectedPickup) {
            selectedPickup = [row, col];
            pickupPosSpan.textContent = `(${row}, ${col})`;
            event.target.classList.add('selected-pickup');
        } else if (!selectedDrop) {
            selectedDrop = [row, col];
            dropPosSpan.textContent = `(${row}, ${col})`;
            event.target.classList.add('selected-drop');
            createTaskBtn.disabled = false;
        }
    }

    function clearSelection() {
        if (selectedPickup) {
            document.getElementById(`cell-${selectedPickup[0]}-${selectedPickup[1]}`)?.classList.remove('selected-pickup');
        }
        if (selectedDrop) {
            document.getElementById(`cell-${selectedDrop[0]}-${selectedDrop[1]}`)?.classList.remove('selected-drop');
        }
        selectedPickup = null;
        selectedDrop = null;
        pickupPosSpan.textContent = 'None';
        dropPosSpan.textContent = 'None';
        createTaskBtn.disabled = true;
    }

    // --- API Communication ---
    async function sendTask() {
        if (!selectedPickup || !selectedDrop) return;
        try {
            await fetch('/add_task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pickup: selectedPickup, drop: selectedDrop }),
            });
            clearSelection();
        } catch (error) {
            console.error("Failed to create task:", error);
        }
    }

    async function sendResetShift() {
        try {
            await fetch('/reset_shift', { method: 'POST' });
            console.log("Reset shift signal sent.");
        } catch (error) {
            console.error("Failed to send reset signal:", error);
        }
    }

    // --- Event Listeners ---
    createTaskBtn.addEventListener('click', sendTask);
    clearSelectionBtn.addEventListener('click', clearSelection);
    resetShiftBtn.addEventListener('click', sendResetShift);

    createTaskBtn.disabled = true;
    initialize();
});

