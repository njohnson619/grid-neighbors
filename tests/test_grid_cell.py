from pytest import fixture

from grid_cli import GridCell

class TestGridCell:

    @fixture
    def cells(self):
        return [GridCell(3, 2, 0), GridCell(1, 5, 7)]

    def test_hash(self, cells):
        cell = cells[0]
        dup_coord = GridCell(cell.row, cell.col, 77)
        dup = GridCell(cell.row, cell.col, cell.value)
        assert len({cell, dup_coord, dup}) == 1

        assert cell == dup_coord
        assert dup == cell
        assert cell == (3, 2)

    def test_distance(self, cells):
        assert cells[0].manhattan_distance(cells[1]) == 5
        assert cells[1].manhattan_distance(cells[0]) == 5

    def test_ops(self, cells):
        assert cells[0] + cells[1] == (4, 7)
        assert cells[0] - cells[1] == (2, -3)
