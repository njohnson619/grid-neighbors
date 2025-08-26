let grid = [];
let rows = 0;
let cols = 0;

function createGrid() {
    rows = parseInt(document.getElementById('rows').value);
    cols = parseInt(document.getElementById('cols').value);
    // max dimensions are defined in html
    if (rows < 1 || cols < 1) {
        alert('Please enter valid grid dimensions (1-50)');
        return;
    }
    
    // Initialize grid with zeros
    grid = Array(rows).fill(null).map(() => Array(cols).fill(0));
    
    // Create HTML grid
    const gridContainer = document.getElementById('gridContainer');
    const gridDiv = document.createElement('div');
    gridDiv.className = 'grid';
    gridDiv.innerHTML = '';
    
    for (let r = 0; r < rows; r++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'grid-row';
        
        for (let c = 0; c < cols; c++) {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'grid-cell';
            cellDiv.dataset.row = r;
            cellDiv.dataset.col = c;
            cellDiv.addEventListener('click', toggleCell);
            rowDiv.appendChild(cellDiv);
        }
        
        gridDiv.appendChild(rowDiv);
    }
    
    gridContainer.innerHTML = '';
    gridContainer.appendChild(gridDiv);
    
    // Enable calculate button
    document.getElementById('calculateBtn').disabled = false;
    
    // Hide results
    document.getElementById('resultSection').style.display = 'none';
}

function toggleCell(event) {
    const row = parseInt(event.target.dataset.row);
    const col = parseInt(event.target.dataset.col);
    
    // Toggle cell value
    grid[row][col] = grid[row][col] > 0 ? 0 : 1;
    
    // Update visual appearance
    if (grid[row][col] > 0) {
        event.target.classList.add('positive');
        event.target.textContent = '+';
    } else {
        event.target.classList.remove('positive');
        event.target.textContent = '';
    }
    
    // Clear neighbor visualization and hide previous results
    clearNeighborVisualization();
    document.getElementById('resultSection').style.display = 'none';
}

function clearGrid() {
    if (grid.length === 0) return;
    
    // Clear grid data
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            grid[r][c] = 0;
        }
    }
    
    // Clear visual grid
    const cells = document.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('positive', 'neighbor');
        cell.textContent = '';
        cell.style.backgroundColor = '';
        cell.title = '';
    });
    
    // Hide results
    document.getElementById('resultSection').style.display = 'none';
}

async function calculateNeighbors() {
    if (grid.length === 0) {
        alert('Please create a grid first');
        return;
    }
    
    const distance = parseInt(document.getElementById('distance').value);
    const algorithm = document.getElementById('algorithm').value;
    const wrapRows = document.getElementById('wrapRows').checked;
    const wrapCols = document.getElementById('wrapCols').checked;
    
    if (distance < 0) {
        alert('Please enter a non-negative distance (0-20)');
        return;
    }
    
    // Check if there are any positive cells
    let hasPositive = false;
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (grid[r][c] > 0) {
                hasPositive = true;
                break;
            }
        }
        if (hasPositive) break;
    }
    
    if (!hasPositive) {
        showResult('No positive cells found in the grid', 'error');
        return;
    }
    
    // Show loading with algorithm info
    showResult(`Calculating using ${algorithm.toUpperCase()} algorithm...`, 'loading');
    
    // Start timing
    const startTime = performance.now();
    
    try {
        const response = await fetch('http://localhost:8000/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grid: grid,
                distance: distance,
                algorithm: algorithm,
                wrap_rows: wrapRows,
                wrap_cols: wrapCols
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Calculate frontend timing
        const endTime = performance.now();
        const frontendTime = endTime - startTime;
        
        if (result.error) {
            showResult(`Error: ${result.error}`, 'error');
        } else {
            // Display neighbors on the grid
            displayNeighbors(result.neighbors);
            
            // Show results with timing information
            const algorithmName = getAlgorithmName(result.algorithm_used);
            
            // Add wrapping info to message
            let wrappingInfo = '';
            if (result.wrap_rows || result.wrap_cols) {
                const wrapTypes = [];
                if (result.wrap_rows) wrapTypes.push('rows');
                if (result.wrap_cols) wrapTypes.push('columns');
                wrappingInfo = ` (with ${wrapTypes.join(' and ')} wrapping)`;
            }
            
            showResult(
                `Number of cells within ${distance} steps of positive values: ${result.count}${wrappingInfo}`, 
                'result',
                algorithmName,
                frontendTime
            );
        }
        
    } catch (error) {
        console.error('Error calculating neighbors:', error);
        showResult(`Error: Could not connect to backend server. Make sure the Python server is running on port 8000.`, 'error');
    }
}

function clearNeighborVisualization() {
    const cells = document.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('neighbor');
        cell.style.backgroundColor = '';
        cell.title = '';
        
        // Preserve positive cell styling
        if (!cell.classList.contains('positive')) {
            cell.textContent = '';
        }
    });
}

function displayNeighbors(neighbors) {
    // First clear any previous neighbor highlighting
    clearNeighborVisualization();
    
    // Color scale for distances (lighter = closer to positive cells)
    const getColorForDistance = (distance, maxDistance) => {
        if (distance === 0) return '#28a745'; // Green for positive cells
        
        // Create a gradient from light blue to dark blue
        const intensity = 1 - (distance / maxDistance);
        const blue = Math.round(255 - (125 * intensity)); // 180-255
        const green = Math.round(255 - (105 * intensity)); // 200-255
        const red = Math.round(255 - (75 * intensity)); // 230-255
        
        return `rgb(${red}, ${green}, ${blue})`;
    };
    
    // Find max distance for color scaling
    const maxDistance = Math.max(...neighbors.map(n => n.distance));
    
    // Apply neighbor styling
    neighbors.forEach(neighbor => {
        const cell = document.querySelector(`[data-row="${neighbor.row}"][data-col="${neighbor.col}"]`);
        if (cell) {
            if (!neighbor.is_positive) {
                cell.classList.add('neighbor');
                cell.style.backgroundColor = getColorForDistance(neighbor.distance, maxDistance);
                cell.textContent = neighbor.distance.toString();
                cell.title = `Distance: ${neighbor.distance} steps from nearest positive cell`;
            } else {
                cell.title = `Positive cell (distance: 0)`;
            }
        }
    });
}

function getAlgorithmName(algorithm) {
    const names = {
        'bfs': 'BFS (Breadth-First Search)',
        'dijkstra': 'Dijkstra',
        'brute_force': 'Brute Force'
    };
    return names[algorithm] || algorithm;
}

function showResult(message, type, algorithmUsed = null, timing = null) {
    const resultSection = document.getElementById('resultSection');
    const resultText = document.getElementById('resultText');
    
    resultText.innerHTML = message;
    
    if (algorithmUsed) {
        resultText.innerHTML += `<span class="algorithm-badge">${algorithmUsed}</span>`;
    }
    
    if (timing !== null) {
        const timingDiv = document.createElement('div');
        timingDiv.className = 'timing-info';
        timingDiv.innerHTML = `
            <strong>Performance:</strong> Calculation completed in ${timing.toFixed(2)} ms
            <br><small>Note: This includes network latency and frontend processing time</small>
        `;
        
        resultText.appendChild(timingDiv);
    }
    
    resultText.className = `result-text ${type}`;
    resultSection.style.display = 'block';
}

// Initialize with a default grid when page loads
window.addEventListener('load', function() {
    createGrid();
});