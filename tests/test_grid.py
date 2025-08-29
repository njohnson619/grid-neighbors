import pytest
from _pytest.fixtures import fixture

from grid_neighbors import Grid


class TestGrid:
    @fixture
    def grid(self):
        return Grid([
            [0, -1, 50],
            [-99, 2, 3],
            [-1, -6, -4]
        ])

    def test_positive_cells(self, grid):
        assert len(grid.positive_cells) == 3

    def test_pretty_print(self, grid):
        print(f"STR: {str(grid)}")
        print(f"REPR: {repr(grid)}")

    def test_get_item(self, grid):
        assert grid[2, 1].value == -6
        assert grid[[2, 1]].value == -6
        assert grid[(2, 1)].value == -6
        with pytest.raises(IndexError):
            _ = grid[44, 8]
        with pytest.raises(IndexError):
            _ = grid[50, 50]
        grid.wrap_rows = True
        assert grid[14, 1].value == -6
        grid.wrap_cols = True
        assert grid[2, 22].value == -6
        assert grid[-1, -1].value == -4

    def test_iter(self, grid):
        assert [c.value for c in grid] == [
            0, -1, 50,
            -99, 2, 3,
            -1, -6, -4
        ]

    def test_off_nominal(self):
        with pytest.raises(RuntimeError, match=r"Invalid cell found"):
            Grid([
                [0, -1, 50],
                ["s", 2, 3],
                [-1, -6, -4]
            ])
        with pytest.raises(RuntimeError, match=r"Invalid grid shape"):
            Grid([
                [0, -1, 50],
                [0, 2],
                [-1, -6, -4]
            ])

