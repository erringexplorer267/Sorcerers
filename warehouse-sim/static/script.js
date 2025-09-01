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
    let obstacles = [];

    // --- Initialization ---
    async function initialize() {
        try {
            const response = await fetch('/init');
            const data = await response.json();
            gridRows = data.grid_size[0];
            gridCols = data.grid_size[1];
            obstacles = data.obstacles;
            createGrid();
            updateGrid(data.robot_positions, []);
            setInterval(mainLoop, data.step_interval || 200);
        } catch (error) {
            console.error("Initialization failed:", error);
        }
    }

    // --- Main Simulation Loop ---
    async function mainLoop() {
        try {
            const response = await fetch('/update');
            const data = await response.json();
            updateGrid(data.robot_positions, data.tasks);
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

    function updateGrid(robots, tasks) {
        document.querySelectorAll('.cell').forEach(cell => {
            cell.className = 'cell';
            cell.textContent = '';
            const r = parseInt(cell.dataset.row);
            const c = parseInt(cell.dataset.col);
            if (obstacles.some(obs => obs[0] === r && obs[1] === c)) {
                cell.classList.add('obstacle');
            }
        });

        tasks.forEach(task => {
            const pickupCell = document.getElementById(`cell-${task.pickup[0]}-${task.pickup[1]}`);
            if (pickupCell) pickupCell.classList.add('task-pickup');

            const dropCell = document.getElementById(`cell-${task.drop[0]}-${task.drop[1]}`);
            if (dropCell) dropCell.classList.add('task-drop');
        });

        robots.forEach(robot => {
            const cell = document.getElementById(`cell-${robot.pos[0]}-${robot.pos[1]}`);
            if (cell) {
                cell.classList.remove('task-pickup', 'task-drop');
                cell.classList.add('robot', `robot-${robot.state}`);
                cell.textContent = `R${robot.id}`;
            }
        });
    }

    // --- User Interaction ---
    function onCellClick(event) {
        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);

        if (event.target.classList.contains('obstacle')) {
            console.warn("Cannot select an obstacle cell.");
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
            await fetch('/reset_shift', {
                method: 'POST'
            });
            console.log("Reset shift signal sent.");
        } catch (error) {
            console.error("Failed to send reset signal:", error);
        }
    }

    // --- Event Listeners ---
    createTaskBtn.addEventListener('click', sendTask);
    clearSelectionBtn.addEventListener('click', clearSelection);
    resetShiftBtn.addEventListener('click', sendResetShift);
    
    initialize();
});

