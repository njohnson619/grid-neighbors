from typing import cast

import pytest

from grid_neighbors.Grid import Grid
from grid_neighbors.neighbor_searches import BruteForceSearch
from utils import assert_count, plot_ascii_table

class TestBruteForce:
    def test_brute_force(self, default):
        result = BruteForceSearch(default, 3).find_neighbors()
        assert_count(result, default, 24, 3)
        plot_ascii_table(default, 3, result)

        result = BruteForceSearch(default, 3, wrap_rows=True).find_neighbors()
        assert_count(result, default, 24, 2, wrap_rows=True)
        result = BruteForceSearch(default, 3, wrap_cols=True).find_neighbors()
        assert_count(result, default, 25, 2, wrap_cols=True)
        result = BruteForceSearch(default, 3, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, default, 25, 2, wrap_rows=True, wrap_cols=True)

        result = BruteForceSearch(default, 1).find_neighbors()
        assert_count(result, default, 10, 1)

    def test_result(self, default):
        neighbors = BruteForceSearch(default, 3).find_neighbors()
        assert_count(neighbors, default, 24, 3)
        fe_result = BruteForceSearch.create_result(neighbors)
        assert fe_result
        assert fe_result["count"] == 24
        assert len(fe_result["positive_cells"]) == 2
        assert len(fe_result["neighbors"]) == 24;

    def test_edges(self, overlapping_edges):
        result = BruteForceSearch(overlapping_edges, 2).find_neighbors()
        assert_count(result, overlapping_edges, 12, 2)

        result = BruteForceSearch(overlapping_edges, 2, wrap_rows=True).find_neighbors()
        assert_count(result, overlapping_edges, 19, 2, wrap_rows=True)
        result = BruteForceSearch(overlapping_edges, 2, wrap_cols=True).find_neighbors()
        assert_count(result, overlapping_edges, 12, 2, wrap_cols=True)
        result = BruteForceSearch(overlapping_edges, 2, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, overlapping_edges, 19, 2, wrap_rows=True, wrap_cols=True)

    def test_adjacent(self, adjacent):
        result = BruteForceSearch(adjacent, 3).find_neighbors()
        assert_count(result, adjacent, 19, 3)

        result = BruteForceSearch(adjacent, 3, wrap_rows=True).find_neighbors()
        assert_count(result, adjacent, 19, 3, wrap_rows=True)
        result = BruteForceSearch(adjacent, 3, wrap_cols=True).find_neighbors()
        assert_count(result, adjacent, 23, 3, wrap_cols=True)
        result = BruteForceSearch(adjacent, 3, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, adjacent, 23, 3, wrap_rows=True, wrap_cols=True)

    def test_corners(self, corners):
        result = BruteForceSearch(corners, 1).find_neighbors()
        assert_count(result, corners, 12, 1)

        result = BruteForceSearch(corners, 2, wrap_rows=True).find_neighbors()
        assert_count(result, corners, 23, 2, wrap_rows=True)
        result = BruteForceSearch(corners, 2, wrap_cols=True).find_neighbors()
        assert_count(result, corners, 22, 2, wrap_cols=True)
        result = BruteForceSearch(corners, 2, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, corners, 23, 2, wrap_rows=True, wrap_cols=True)

    def test_odd_shapes(self, odd_shapes):
        dist = [2, 2, 4]
        expected = [4, 3, 1]
        for i in range(len(odd_shapes)):
            grid, n, exp = odd_shapes[i], dist[i], expected[i]
            result = BruteForceSearch(grid, n).find_neighbors()
            assert len(result) == exp, f"Failed on {grid=}, {n=}, {exp=}, {result=}"

    def test_off_nominal(self, default):
        with pytest.raises(RuntimeError, match=r"Grid not specified or empty"):
            BruteForceSearch(cast(Grid, None), 1).find_neighbors()
        with pytest.raises(RuntimeError, match=r"Grid not specified or empty"):
            BruteForceSearch([], 1).find_neighbors()
        with pytest.raises(RuntimeError, match=r"Empty row\(s\)"):
            BruteForceSearch([[]], 1).find_neighbors()
        neighbors = BruteForceSearch([[0, 0], [0, 0]], 1).find_neighbors()
        result = BruteForceSearch.create_result(neighbors)
        assert result["count"] == 0, f"Expected 0 neighbors, got {result}"
        assert result["positive_cells"] == [], f"Expected empty positive cells, got {result}"
        assert result["neighbors"] == [], f"Expected empty neighbors, got {result}"
        neighbors = BruteForceSearch(default, default.num_cols * default.num_rows).find_neighbors()
        result = BruteForceSearch.create_result(neighbors)
        assert result["count"] == default.num_rows*default.num_cols
        neighbors = BruteForceSearch(default, 0).find_neighbors()
        result = BruteForceSearch.create_result(neighbors)
        assert result["count"] == 2
        assert len(result["positive_cells"]) == 2
        assert len(result["neighbors"]) == 2
        with pytest.raises(ValueError, match=r"Max distance must be non-negative"):
            BruteForceSearch(default, -1).find_neighbors()
