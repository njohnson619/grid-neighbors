from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq
from collections import deque

from src.grid_neighbors import Grid, BruteForce

app = Flask(__name__)
CORS(app)

# def manhattan_distance_with_wrapping(r1, c1, r2, c2, rows, cols, wrap_rows=False, wrap_cols=False):
#     """
#     Calculate Manhattan distance between two points, optionally with wrapping.
#
#     Args:
#         r1, c1: First point coordinates
#         r2, c2: Second point coordinates
#         rows, cols: Grid dimensions
#         wrap_rows: If True, rows wrap around (toroidal row wrapping)
#         wrap_cols: If True, columns wrap around (toroidal column wrapping)
#
#     Returns:
#         Minimum Manhattan distance considering wrapping
#     """
#     # Calculate row distance
#     if wrap_rows:
#         row_dist = min(abs(r1 - r2), rows - abs(r1 - r2))
#     else:
#         row_dist = abs(r1 - r2)
#
#     # Calculate column distance
#     if wrap_cols:
#         col_dist = min(abs(c1 - c2), cols - abs(c1 - c2))
#     else:
#         col_dist = abs(c1 - c2)
#
#     return row_dist + col_dist

# def get_neighbors_with_wrapping(r, c, rows, cols, wrap_rows=False, wrap_cols=False):
#     """
#     Get the 4-connected neighbors of a cell, considering wrapping.
#
#     Args:
#         r, c: Current cell coordinates
#         rows, cols: Grid dimensions
#         wrap_rows: If True, rows wrap around
#         wrap_cols: If True, columns wrap around
#
#     Returns:
#         List of (row, col) tuples for valid neighbors
#     """
#     neighbors = []
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
#
#     for dr, dc in directions:
#         new_r = r + dr
#         new_c = c + dc
#
#         # Handle row wrapping
#         if wrap_rows:
#             new_r = new_r % rows
#         elif new_r < 0 or new_r >= rows:
#             continue
#
#         # Handle column wrapping
#         if wrap_cols:
#             new_c = new_c % cols
#         elif new_c < 0 or new_c >= cols:
#             continue
#
#         neighbors.append((new_r, new_c))
#
#     return neighbors

def calculate_neighbors_brute_force(grid: Grid, distance_threshold: int, wrap_rows=False, wrap_cols=False):
    """
    BRUTE FORCE ALGORITHM - O(R×C×P) time complexity
    Calculate the cells that fall within N steps of any positive values in the array.
    
    Args:
        grid: 2D array where positive values are the starting points
        distance_threshold: Maximum Manhattan distance (N)
        wrap_rows: If True, rows wrap around (toroidal)
        wrap_cols: If True, columns wrap around (toroidal)
    
    Returns:
        Dictionary with count and detailed neighbor information
    """
    return BruteForce(grid, distance_threshold, wrap_rows, wrap_cols).find_neighbors()
# def calculate_neighbors_bfs(grid, distance_threshold, wrap_rows=False, wrap_cols=False):
#     """
#     MULTI-SOURCE BFS ALGORITHM - O(R×C) time complexity
#     Use breadth-first search starting from all positive cells simultaneously.
#     Each BFS level represents cells at distance 1, 2, 3, etc. from nearest positive cell.
#
#     Args:
#         grid: 2D array where positive values are the starting points
#         distance_threshold: Maximum Manhattan distance (N)
#         wrap_rows: If True, rows wrap around (toroidal)
#         wrap_cols: If True, columns wrap around (toroidal)
#
#     Returns:
#         Dictionary with count and detailed neighbor information
#     """
#     if not grid or not grid[0]:
#         return {'count': 0, 'neighbors': [], 'positive_cells': []}
#
#     rows = len(grid)
#     cols = len(grid[0])
#
#     # Find all positive cells
#     positive_cells = []
#     queue = deque()
#     distances = {}
#
#     for r in range(rows):
#         for c in range(cols):
#             if grid[r][c] > 0:
#                 positive_cells.append({'row': r, 'col': c})
#                 queue.append((r, c, 0))  # (row, col, distance)
#                 distances[(r, c)] = 0
#
#     if not positive_cells:
#         return {'count': 0, 'neighbors': [], 'positive_cells': []}
#
#     # Multi-source BFS
#     while queue:
#         current_r, current_c, current_dist = queue.popleft()
#
#         # Skip if we've exceeded the distance threshold
#         if current_dist >= distance_threshold:
#             continue
#
#         # Explore all neighbors (with wrapping support)
#         for new_r, new_c in get_neighbors_with_wrapping(current_r, current_c, rows, cols, wrap_rows, wrap_cols):
#             new_dist = current_dist + 1
#
#             # If we haven't visited this cell
#             if (new_r, new_c) not in distances:
#                 distances[(new_r, new_c)] = new_dist
#                 queue.append((new_r, new_c, new_dist))
#
#     # Convert to result format
#     neighbors = []
#     for (r, c), distance in distances.items():
#         if distance <= distance_threshold:
#             neighbors.append({
#                 'row': r,
#                 'col': c,
#                 'distance': distance,
#                 'is_positive': grid[r][c] > 0
#             })
#
#     return {
#         'count': len(neighbors),
#         'neighbors': neighbors,
#         'positive_cells': positive_cells
#     }
#
# def calculate_neighbors_dijkstra(grid, distance_threshold, wrap_rows=False, wrap_cols=False):
#     """
#     PRIORITY QUEUE (DIJKSTRA-LIKE) ALGORITHM - O(R×C×log(R×C)) time complexity
#     Use a priority queue (min-heap) to process cells in order of increasing distance.
#     Guarantees optimal distances and can handle weighted edges easily.
#
#     Args:
#         grid: 2D array where positive values are the starting points
#         distance_threshold: Maximum Manhattan distance (N)
#         wrap_rows: If True, rows wrap around (toroidal)
#         wrap_cols: If True, columns wrap around (toroidal)
#
#     Returns:
#         Dictionary with count and detailed neighbor information
#     """
#     if not grid or not grid[0]:
#         return {'count': 0, 'neighbors': [], 'positive_cells': []}
#
#     rows = len(grid)
#     cols = len(grid[0])
#
#     # Find all positive cells
#     positive_cells = []
#     heap = []  # Priority queue: (distance, row, col)
#     distances = {}
#
#     for r in range(rows):
#         for c in range(cols):
#             if grid[r][c] > 0:
#                 positive_cells.append({'row': r, 'col': c})
#                 heapq.heappush(heap, (0, r, c))
#                 distances[(r, c)] = 0
#
#     if not positive_cells:
#         return {'count': 0, 'neighbors': [], 'positive_cells': []}
#
#     # Dijkstra directions: up, down, left, right (Manhattan distance neighbors)
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#
#     # Process cells in order of increasing distance
#     while heap:
#         current_dist, current_r, current_c = heapq.heappop(heap)
#
#         # Skip if we already found a better path to this cell
#         if current_dist > distances.get((current_r, current_c), float('inf')):
#             continue
#
#         # Skip if we've exceeded the distance threshold
#         if current_dist >= distance_threshold:
#             continue
#
#         # Explore all neighbors (with wrapping support)
#         for new_r, new_c in get_neighbors_with_wrapping(current_r, current_c, rows, cols, wrap_rows, wrap_cols):
#             new_dist = current_dist + 1
#
#             # Check distance threshold and if we found a shorter path
#             if (new_dist <= distance_threshold and
#                 new_dist < distances.get((new_r, new_c), float('inf'))):
#                 distances[(new_r, new_c)] = new_dist
#                 heapq.heappush(heap, (new_dist, new_r, new_c))
#
#     # Convert to result format
#     neighbors = []
#     for (r, c), distance in distances.items():
#         neighbors.append({
#             'row': r,
#             'col': c,
#             'distance': distance,
#             'is_positive': grid[r][c] > 0
#         })
#
#     return {
#         'count': len(neighbors),
#         'neighbors': neighbors,
#         'positive_cells': positive_cells
#     }

def calculate_neighbors(grid, distance_threshold, algorithm='bfs', wrap_rows=False, wrap_cols=False):
    """
    Calculate neighbors using the specified algorithm.
    
    Args:
        grid: 2D array where positive values are the starting points
        distance_threshold: Maximum Manhattan distance (N)
        algorithm: 'brute_force', 'bfs', or 'dijkstra'
        wrap_rows: If True, rows wrap around (toroidal)
        wrap_cols: If True, columns wrap around (toroidal)
    
    Returns:
        Dictionary with count and detailed neighbor information
    """
    if algorithm == 'brute_force':
        result = calculate_neighbors_brute_force(grid, distance_threshold, wrap_rows, wrap_cols)
        return result
    # elif algorithm == 'bfs':
    #     return calculate_neighbors_bfs(grid, distance_threshold, wrap_rows, wrap_cols)
    # elif algorithm == 'dijkstra':
    #     return calculate_neighbors_dijkstra(grid, distance_threshold, wrap_rows, wrap_cols)
    else:
        # # Default to BFS (most efficient for this problem)
        # return calculate_neighbors_bfs(grid, distance_threshold, wrap_rows, wrap_cols)
        return {"count": 0, "neighbors": [], "positive_cells": []}

@app.route('/calculate', methods=['POST'])
def calculate_endpoint():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        grid_data = data.get('grid')
        distance = data.get('distance')
        algorithm = data.get('algorithm', 'brute_force')  # Default to brute force
        wrap_rows = data.get('wrap_rows', False)
        wrap_cols = data.get('wrap_cols', False)
        
        if grid_data is None:
            return jsonify({'error': 'Grid data is required'}), 400
        
        if distance is None:
            return jsonify({'error': 'Distance parameter is required'}), 400
        
        if not isinstance(distance, int) or distance < 0:
            return jsonify({'error': 'Distance must be a non-negative integer'}), 400
        
        # Validate algorithm parameter
        valid_algorithms = ['brute_force', 'bfs', 'dijkstra']
        if algorithm not in valid_algorithms:
            return jsonify({'error': f'Algorithm must be one of: {valid_algorithms}'}), 400
        
        try:
            # data is validated inside the Grid init
            grid = Grid(grid_data)
        except RuntimeError as re:
            return jsonify({'error': str(re)}), 400

        # Calculate the result using the specified algorithm
        result = calculate_neighbors(grid, distance, algorithm, wrap_rows, wrap_cols)
        
        return jsonify({
            'count': result['count'],
            'neighbors': result['neighbors'],
            'positive_cells': result['positive_cells'],
            'grid_size': f"{len(grid_data)}x{len(grid_data[0])}",
            'distance_threshold': distance,
            'algorithm_used': algorithm,
            'wrap_rows': wrap_rows,
            'wrap_cols': wrap_cols
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Grid neighbors API is running'})

if __name__ == '__main__':
    print("Starting Grid Cell Neighborhoods API...")
    print("Open http://localhost:8000/health to check if the server is running")
    print("Frontend should be accessible by opening index.html in a web browser")
    app.run(debug=True, host='0.0.0.0', port=8000)