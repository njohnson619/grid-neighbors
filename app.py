import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

from src.grid_neighbors.neighbor_searches import BreadthFirstSearch
from src.grid_neighbors.Logger import set_global_log_level
from src.grid_neighbors import Grid, BruteForceSearch

app = Flask(__name__)
CORS(app)

# usually log level is defined in environment
set_global_log_level(logging.DEBUG)


def calculate_neighbors_bfs(grid: Grid, distance_threshold: int):
    """
    MULTI-SOURCE BFS ALGORITHM - O(R×C) time complexity
    Use breadth-first search starting from all positive cells simultaneously.
    Each BFS level represents cells at distance 1, 2, 3, etc. from nearest positive cell.

    Args:
        grid: Grid object with data, wrapping, and distance type configuration
        distance_threshold: Maximum distance (N) based on the grid's distance type

    Returns:
        Dictionary with count and detailed neighbor information
    """
    neighbors = BreadthFirstSearch(grid, distance_threshold, grid.wrap_rows, grid.wrap_cols).find_neighbors()
    return BreadthFirstSearch.create_result(neighbors)

def calculate_neighbors_brute_force(grid: Grid, distance_threshold: int):
    """
    BRUTE FORCE ALGORITHM - O(R×C×P) time complexity
    Calculate the cells that fall within N steps of any positive values in the array.

    Args:
        grid: Grid object with data, wrapping, and distance type configuration
        distance_threshold: Maximum distance (N) based on the grid's distance type

    Returns:
        Dictionary with count and detailed neighbor information
    """
    neighbors = BruteForceSearch(grid, distance_threshold, grid.wrap_rows, grid.wrap_cols).find_neighbors()
    return BruteForceSearch.create_result(neighbors)

def calculate_neighbors(grid, distance_threshold, algorithm='bfs'):
    """
    Calculate neighbors using the specified algorithm.
    
    Args:
        grid: Grid object with data, wrapping, and distance type configuration
        distance_threshold: Maximum distance (N) based on the grid's distance type
        algorithm: 'brute_force', 'bfs', or 'dijkstra'
    
    Returns:
        Dictionary with count and detailed neighbor information
    """
    if algorithm == 'brute_force':
        return calculate_neighbors_brute_force(grid, distance_threshold)
    elif algorithm == 'bfs':
        return calculate_neighbors_bfs(grid, distance_threshold)
    else:
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
        distance_type = data.get('distance_type', 'manhattan')  # Default to manhattan
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
        
        # Validate distance_type parameter
        valid_distance_types = ['manhattan', 'chebyshev']
        if distance_type not in valid_distance_types:
            return jsonify({'error': f'Distance type must be one of: {valid_distance_types}'}), 400
        
        try:
            # data is validated inside the Grid init
            grid = Grid(grid_data, wrap_rows, wrap_cols, distance_type)
        except RuntimeError as re:
            return jsonify({'error': str(re)}), 400

        # Calculate the result using the specified algorithm
        result = calculate_neighbors(grid, distance, algorithm)
        
        return jsonify({
            'count': result['count'],
            'neighbors': result['neighbors'],
            'positive_cells': result['positive_cells'],
            'grid_size': f"{len(grid_data)}x{len(grid_data[0])}",
            'distance_threshold': distance,
            'algorithm_used': algorithm,
            'distance_type': distance_type,
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