import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq
from collections import deque

from src.grid_neighbors.Logger import set_global_log_level
from src.grid_neighbors import Grid, BruteForce

app = Flask(__name__)
CORS(app)

# usually log level is defined in environment
set_global_log_level(logging.DEBUG)


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