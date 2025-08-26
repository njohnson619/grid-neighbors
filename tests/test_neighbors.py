from typing import cast

import pytest
from _pytest.fixtures import fixture

from grid_neighbors.Grid import Grid
from grid_neighbors.neighbor_searches import BruteForce

class TestNeighbors:
    @fixture
    def default(self):
        return Grid([
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ])

    @fixture
    def overlapping_edges(self):
        return Grid([
            [0, 1, 0, 1, 0],
            [0,-1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0,-1,-2, 0],
            [0, 0, 0, 0, 0],
        ])

    @fixture
    def adjacent(self):
        return Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 5, 8, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])

    @fixture
    def corners(self):
        return Grid([
            [1, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [4, 0, 3, 0, 0],
        ])

    @fixture
    def odd_shapes(self):
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

    def test_brute_force(self, default):
        result = BruteForce(default, 3).find_neighbors()
        assert result and result["count"] == 24

        result = BruteForce(default, 1).find_neighbors()
        assert result and result["count"] == 10

    def test_edges(self, overlapping_edges):
        result = BruteForce(overlapping_edges, 2).find_neighbors()
        assert result and result["count"] == 12

    def test_adjacent(self, adjacent):
        result = BruteForce(adjacent, 3).find_neighbors()
        assert result and result["count"] == 23

    def test_corners(self, corners):
        result = BruteForce(corners, 1).find_neighbors()
        assert result and result["count"] == 12

    def test_odd_shapes(self, odd_shapes):
        dist = [2, 2, 4]
        expected = [4, 3, 1]
        for i in range(len(odd_shapes)):
            grid, n, exp = odd_shapes[i], dist[i], expected[i]
            result = BruteForce(grid, n).find_neighbors()
            assert result and result["count"] == exp, f"Failed on {grid=}, {n=}, {exp=}, {result=}"

    def test_off_nominal(self, default):
        with pytest.raises(RuntimeError, match=r"Grid not specified or empty"):
            BruteForce(cast(Grid, None), 1).find_neighbors()
        with pytest.raises(RuntimeError, match=r"Grid not specified or empty"):
            BruteForce([], 1).find_neighbors()
        with pytest.raises(RuntimeError, match=r"Grid not specified or empty"):
            BruteForce([[]], 1).find_neighbors()
        BruteForce([[0, 0], [0, 0]], 1).find_neighbors()
        BruteForce(default, default.num_cols*default.num_rows).find_neighbors()
        BruteForce(default, 0).find_neighbors()
        BruteForce(default, -1).find_neighbors()
