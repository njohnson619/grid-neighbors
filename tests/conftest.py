import os
import sys

from pytest import fixture

# Add the project source code to the python path so the tests have direct access.
# Note: this assumes the tests directory is at the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(project_root, "src"))

# also add top level test utilities
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from grid_neighbors import Grid

@fixture
def default():
    return Grid([
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ])

@fixture
def overlapping_edges():
    return Grid([
        [0, 1, 0, 1, 0],
        [0,-1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0,-1,-2, 0],
        [0, 0, 0, 0, 0],
    ])

@fixture
def adjacent():
    return Grid([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [5, 8, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ])

@fixture
def corners():
    return Grid([
        [1, 0, 0, 0, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [4, 0, 3, 0, 0],
    ])

@fixture
def odd_shapes():
    return [
        Grid([
            [0, 1, 0, 0, 0],
        ]),
        Grid([
            [1],
            [0],
            [0],
            [0],
        ]),
        Grid([
            [1],
        ])
    ]
