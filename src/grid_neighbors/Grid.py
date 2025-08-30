from numbers import Number
from typing import Tuple, Iterator, Sequence, TypeAlias, Optional

from .GridCell import GridCell

Matrix: TypeAlias = Sequence[Sequence[Number]]


class Grid:
    """
    Read-only viewer for a two-dimensional matrix of numbers.

    The matrix is indexed as a table of rows and columns. Each dimension has the option of wrapping indices from
    back to front. Numbers are encapsulated in GridCell objects when accessed that contain the value, row, and column.
    """
    # unit vectors for cardinal directions given row, col indices.
    NW_DIR = 1, -1
    N_DIR = -1, 0
    NE_DIR = 1, 1
    E_DIR = 0, 1
    SE_DIR = -1, 1
    S_DIR = 1, 0
    SW_DIR = -1, -1
    W_DIR = 0, -1

    DISTANCE_TYPES = {
        "manhattan": "manhattan_distance",
        "chebyshev": "chebyshev_distance",
    }

    def __init__(
        self,
        data: Matrix,
        wrap_rows: bool = False,
        wrap_cols: bool = False,
        distance_type: Optional[str]=None
    ):
        # expect caller to provide consistent grid. methods assume this validation exists
        self._validate_grid(data)
        # store reference instead of copying to save time and memory. this means that methods
        # can't assume the grid remains unchanged between calls.
        self._data = data
        self.wrap_rows = wrap_rows
        self.wrap_cols = wrap_cols
        self.distance_type = distance_type or "manhattan"

    def __str__(self):
        r_str = f"R" if self.wrap_rows else f"_"
        c_str = f"C" if self.wrap_cols else f"_"
        return f"Grid[{r_str}{c_str}] ({self.num_rows} X {self.num_cols})"

    def __repr__(self):
        vals_str = "\n".join([" ".join(f"{val:>4}" for val in row) for row in self._data])
        return f"{str(self)}\n{vals_str}"

    def __getitem__(self, row_col: Sequence[int]):
        """Enable `grid[row, col]` syntax for cell-specific values"""
        if not isinstance(row_col, Sequence) or len(row_col) != 2:
            raise TypeError(f"Row/Column must be a sequence (len 2). Received {type(row_col)}, {row_col}")
        row, col = self._validate_indices(*row_col)
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
    def num_cells(self) -> int:
        return self.num_rows * self.num_cols

    @property
    def positive_cells(self) -> list[GridCell]:
        return [cell for cell in self if cell.value > 0]

    def get_immediate_neighbors(
        self,
        center_cell: GridCell,
    ) -> Sequence["GridCell"]:
        neighbors = []
        directions = [
            self.N_DIR, self.S_DIR, self.W_DIR, self.E_DIR
        ] if self.distance_type == "manhattan" else [
            self.N_DIR, self.S_DIR, self.W_DIR, self.E_DIR,
            self.NW_DIR, self.NE_DIR, self.SW_DIR, self.SE_DIR
        ]
        for direction in directions:
            try:
                # [] method is smart enough to wrap indexes when needed
                neighbors.append(self[(center_cell + direction).coords])
            except IndexError:
                # neighbor is out of bounds and therefore doesn't exist
                continue
        return neighbors

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
        # Non-Empty
        if row_lengths[0] == 0:
            raise RuntimeError(f"Empty row(s). Row lengths: {row_lengths}")
        # Cells
        for row in grid:
            for cell in row:
                if not isinstance(cell, Number):
                    raise RuntimeError(f"Invalid cell found: {cell}")

    def _validate_indices(self, row: int, col: int) -> tuple[int, int]:
        """
        Validate and modify (if necessary) the specified row/col to access
        the source data matrix.
        """
        row_index = row % self.num_rows if self.wrap_rows else row
        col_index = col % self.num_cols if self.wrap_cols else col
        if row_index < 0 or row_index >= self.num_rows or col_index < 0 or col_index >= self.num_cols:
            raise IndexError(f"Invalid row/col: ({row},{col}) for {str(self)}")
        return row_index, col_index

