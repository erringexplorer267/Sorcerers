document.addEventListener('DOMContentLoaded', () => {
    const gridDiv = document.getElementById('grid');
    const createTaskBtn = document.getElementById('create-task-btn');
    const clearSelectionBtn = document.getElementById('clear-selection-btn');
    const pickupPosSpan = document.getElementById('pickup-pos');
    const dropPosSpan = document.getElementById('drop-pos');

    let gridRows = 0;
    let gridCols = 0;
    let selectedPickup = null;
    let selectedDrop = null;
    let stepInterval = 200;

    
    async function initialize() {
        try {
            const response = await fetch('/init');
            const data = await response.json();
            gridRows = data.grid_size[0];
            gridCols = data.grid_size[1];
            stepInterval = data.step_interval || 200;
            createGrid();
            updateGrid(data.robot_positions, []);
            // Start the main simulation loop
            setInterval(mainLoop, stepInterval);
        } catch (error) {
            console.error("Initialization failed:", error);
        }
    }

    async function mainLoop() {
        try {
            const response = await fetch('/update');
            const data = await response.json();
            updateGrid(data.robot_positions, data.tasks);
        } catch (error) {
            console.error("Error fetching update:", error);
        }
    }


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
                cell.classList.add('robot');
                if (robot.state === 'moving_to_pickup') {
                    cell.classList.add('robot-pickup');
                } else if (robot.state === 'moving_to_drop') {
                    cell.classList.add('robot-drop');
                } else {
                    cell.classList.add('robot-idle');
                }
                cell.textContent = `R${robot.id}`;
            }
        });
    }



    function onCellClick(event) {
        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);

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
        if(selectedPickup) {
            const pickupCell = document.getElementById(`cell-${selectedPickup[0]}-${selectedPickup[1]}`);
            if(pickupCell) pickupCell.classList.remove('selected-pickup');
        }
        if(selectedDrop) {
            const dropCell = document.getElementById(`cell-${selectedDrop[0]}-${selectedDrop[1]}`);
            if(dropCell) dropCell.classList.remove('selected-drop');
        }

        selectedPickup = null;
        selectedDrop = null;
        pickupPosSpan.textContent = 'None';
        dropPosSpan.textContent = 'None';
        createTaskBtn.disabled = true;
    }

    async function sendTask() {
        if (!selectedPickup || !selectedDrop) {
            alert("Please select both a pickup and drop-off location.");
            return;
        }

        try {
            const response = await fetch('/add_task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    pickup: selectedPickup,
                    drop: selectedDrop,
                }),
            });
            const result = await response.json();
            console.log("Task creation:", result.message);
            clearSelection();
        } catch (error) {
            console.error("Failed to create task:", error);
        }
    }


    createTaskBtn.addEventListener('click', sendTask);
    createTaskBtn.disabled = true;
    clearSelectionBtn.addEventListener('click', clearSelection);

    initialize();
});
