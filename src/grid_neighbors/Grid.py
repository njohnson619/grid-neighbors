from numbers import Number
from typing import Tuple, Iterator, Sequence, TypeAlias

from grid_neighbors.GridCell import GridCell

Matrix: TypeAlias = Sequence[Sequence[Number]]


class Grid:
    """
    Read-only viewer for a two-dimensional matrix of numbers.

    Provides basic validation and syntatic sugar for accessing individual cells.
    """
    def __init__(self, data: Matrix):
        # expect caller to provide consistent grid. methods assume this validation exists
        self._validate_grid(data)
        # store reference instead of copying to save time and memory. this means that methods
        # can't assume the grid remains unchanged between calls.
        self._data = data

    def __str__(self):
        return f"Grid [{self.num_rows} X {self.num_cols}]"

    def __repr__(self):
        vals_str = "\n".join([" ".join(f"{val:>4}" for val in row) for row in self._data])
        return f"{str(self)}\n{vals_str}"

    def __getitem__(self, row_col):
        """Enable `grid[row, col]` syntax for cell-specific values"""
        if not isinstance(row_col, tuple):
            raise ValueError(f"Row/Column must be tuple. Received {type(row_col)}, {row_col}")
        self._validate_indices(*row_col)

        row, col = row_col
        return GridCell(row, col, self._data[row][col])

    def __iter__(self) -> Iterator[GridCell]:
        """
        Yield GridCell object for all elements in the grid.

        Grid is traversed in row-major order.
        """
        for row_idx, row in enumerate(self._data):
            for col_idx, value in enumerate(row):
                yield self[row_idx, col_idx]

    @property
    def shape(self) -> Tuple[int, int]:
        # because data isn't owned by this class and can change externally,
        # calculate dimensions on each call (trade performance for robustness).
        return len(self._data), len(self._data[0])

    @property
    def num_rows(self) -> int:
        return self.shape[0]

    @property
    def num_cols(self) -> int:
        return self.shape[1]

    @property
    def positive_cells(self) -> Sequence[GridCell]:
        return [cell for cell in self if cell.value > 0]

    def _validate_grid(self, grid: Matrix) -> None:
        """
        Validate expected requirements of grid.

        For simplicity, an invalid grid is a fatal error and stops execution.
        # TODO: Derive from pydantic BaseModel for standard/consistent validation protocol
        """
        # Existence
        if not grid:
            raise RuntimeError(f"Grid not specified or empty: {grid}")
        # Shape
        row_lengths = [len(row) for row in grid]
        if len(set(row_lengths)) != 1:
            raise RuntimeError(f"Invalid grid shape. Row lengths: {row_lengths}")
        # Cells
        for row in grid:
            for cell in row:
                if not isinstance(cell, Number):
                    raise RuntimeError(f"Invalid cell found: {cell}")

    def _validate_indices(self, row: int, col: int) -> bool:
        """
        Indices must be within range of a standard matrix.

        Caller must convert indices when using algorithms with wrapping edges.
        """
        if not (0 <= row < self.num_rows and 0 <= col < self.num_cols):
            raise RuntimeError(f"Invalid row/col: ({row},{col})")

