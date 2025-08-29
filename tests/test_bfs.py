from grid_neighbors.neighbor_searches import BreadthFirstSearch

from utils import assert_count


class TestBFS:
    def test_default(self, default):
        result = BreadthFirstSearch(default, 3).find_neighbors()
        assert_count(result, default, 24, 3)

        result = BreadthFirstSearch(default, 3, wrap_rows=True).find_neighbors()
        assert_count(result, default, 24, 2, wrap_rows=True)
        result = BreadthFirstSearch(default, 3, wrap_cols=True).find_neighbors()
        assert_count(result, default, 25, 2, wrap_cols=True)
        result = BreadthFirstSearch(default, 3, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, default, 25, 2, wrap_rows=True, wrap_cols=True)

        result = BreadthFirstSearch(default, 1).find_neighbors()
        assert_count(result, default, 10, 1)

    def test_edges(self, overlapping_edges):
        result = BreadthFirstSearch(overlapping_edges, 2).find_neighbors()
        assert_count(result, overlapping_edges, 12, 2)

        result = BreadthFirstSearch(overlapping_edges, 2, wrap_rows=True).find_neighbors()
        assert_count(result, overlapping_edges, 19, 2, wrap_rows=True)
        result = BreadthFirstSearch(overlapping_edges, 2, wrap_cols=True).find_neighbors()
        assert_count(result, overlapping_edges, 12, 2, wrap_cols=True)
        result = BreadthFirstSearch(overlapping_edges, 2, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, overlapping_edges, 19, 2, wrap_rows=True, wrap_cols=True)

    def test_adjacent(self, adjacent):
        result = BreadthFirstSearch(adjacent, 3).find_neighbors()
        assert_count(result, adjacent, 19, 3)

        result = BreadthFirstSearch(adjacent, 3, wrap_rows=True).find_neighbors()
        assert_count(result, adjacent, 19, 3, wrap_rows=True)
        result = BreadthFirstSearch(adjacent, 3, wrap_cols=True).find_neighbors()
        assert_count(result, adjacent, 23, 3, wrap_cols=True)
        result = BreadthFirstSearch(adjacent, 3, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, adjacent, 23, 3, wrap_rows=True, wrap_cols=True)

    def test_corners(self, corners):
        result = BreadthFirstSearch(corners, 1).find_neighbors()
        assert_count(result, corners, 12, 1)

        result = BreadthFirstSearch(corners, 2, wrap_rows=True).find_neighbors()
        assert_count(result, corners, 23, 2, wrap_rows=True)
        result = BreadthFirstSearch(corners, 2, wrap_cols=True).find_neighbors()
        assert_count(result, corners, 22, 2, wrap_cols=True)
        result = BreadthFirstSearch(corners, 2, wrap_rows=True, wrap_cols=True).find_neighbors()
        assert_count(result, corners, 23, 2, wrap_rows=True, wrap_cols=True)

    def test_odd_shapes(self, odd_shapes):
        dist = [2, 2, 4]
        expected = [4, 3, 1]
        for i in range(len(odd_shapes)):
            grid, n, exp = odd_shapes[i], dist[i], expected[i]
            result = BreadthFirstSearch(grid, n).find_neighbors()
            assert len(result) == exp, f"Failed on {grid=}, {n=}, {exp=}, {result=}"
