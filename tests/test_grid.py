import pytest
from _pytest.fixtures import fixture

from grid_cli.Grid import Grid


class TestGrid:
    def test_positive_cells(self):
        with pytest.raises(RuntimeError, match=r"Invalid cell found"):
            Grid([
                [0, -1, 50],
                ["s", 2, 3],
                [-1, -6, -4]
            ])
        g = Grid([
            [0, -1, 50],
            [-99, 2, 3],
            [-1, -6, -4]
        ])
        assert len(g.positive_cells) == 3

    def test_sources_included(self):
        pass

    def test_unique_sources(self):
        # pass duplicate sources to neighbors method

        # assert only one source exists in result
        pass

    @fixture
    def grid(self):
        return Grid([
            [0, -1, 50],
            [-99, 2, 3],
            [-1, -6, -4]
        ])

    def test_pretty_print(self, grid):
        print(f"STR: {str(grid)}")
        print(f"REPR: {repr(grid)}")

    def test_get_item(self, grid):
        assert grid[2, 1].value == -6
        with pytest.raises(RuntimeError, match=r"Invalid row/col"):
            _ = grid[44, 8]

    def test_iter(self, grid):
        assert [c.value for c in grid] == [
            0, -1, 50,
            -99, 2, 3,
            -1, -6, -4
        ]
