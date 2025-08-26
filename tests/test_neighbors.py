import pytest
from _pytest.fixtures import fixture

from grid_neighbors.Grid import Grid
from grid_neighbors.neighbor_searches import BruteForce

class TestNeighbors:
    @fixture
    def grid(self):
        return Grid([
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ])

    def test_brute_force(self, grid):
        n = 3
        bf = BruteForce(grid, n)
        result = bf.find_neighbors()
        assert result and result["count"] == 24

        n = 1
        bf = BruteForce(grid, n)
        result = bf.find_neighbors()
        assert result and result["count"] == 10
